import scrapy
import re 

class EtudiantSpider(scrapy.Spider):
    name = 'etudiantscraper'
    start_urls = ["https://www.letudiant.fr/lycee/annuaire-des-lycees.html"]

    def info_box(self, etablissement):
        info = {
            'nom': self.clear_info(etablissement.css('h2::text').get()),
            'diplome': self.clear_info(etablissement.css('li.tw-bg-black::text').get()),
            'statut': self.clear_info(etablissement.css('li.tw-bg-primary::text').get()),
            'ville': self.clear_info(etablissement.css('span.tw-text-sans::text').get()),
            'nombre_etoiles': self.clear_info(etablissement.css('span.tw-mr-2.tw-font-heading.tw-leading-6.tw-text-2xl.tw-ml-1::text').get()),
            'nombre_commentaires': self.clear_info(etablissement.css('span.tw-pl-3::text').get()),
        }
        return info

    def second_box(self, etablissement):
        elements = etablissement.css("div.tw-w-1\/3.tw-pl-5.tw-pt-3")
        return {
            'classement': elements[0].css("span::text").get(),
            'mention': elements[1].css("span::text").get(),
            'specialite': elements[2].css("span::text").get()
        }

    def clear_info(self, info):
        if info is not None:
            return info.strip()

    def parse(self, response):
        # Trouver les liens vers toutes les régions et les suivre
        all_region = response.css('div.tw-pb-6.sm\\:tw-pb-12.tw-grid.sm\\:tw-grid-cols-3.grid-cols-1.tw-text-sm')
        region_links = all_region.css('a::attr(href)').getall()
        region_links = list(set([lien for lien in region_links if '/lycee/annuaire-des-lycees/departement' in lien]))
        for region_link in region_links:
            yield response.follow(region_link, callback=self.parse_region)

    def parse_region(self, response):
        # Itérer sur chaque établissement de la région et suivre les liens de détail
        for etablissement_link in response.css('a[title][href*="/fiche/"]'):
            detail_link = etablissement_link.attrib['href']
            if detail_link:
                etablissement = etablissement_link.css('.tw-border-solid.tw-border.tw-border-gray-500.tw-rounded-large')
                first_box = self.info_box(etablissement.css("div.tw-relative.tw-w-full"))
                second_box = self.second_box(etablissement.css("div.tw-w-full.tw-flex"))
                yield response.follow(detail_link, callback=self.parse_etablissement_detail, meta={'first_box': first_box, 'second_box': second_box})

            next_page = response.xpath('//i[contains(@class, "fa-chevron-right")]/parent::a/@href').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse_region)

    def parse_etablissement_detail(self, response):
        # Récupérer les données transmises via meta et les combiner
        first_box = response.meta['first_box']
        second_box = response.meta['second_box']
        adresse_elements = response.css('div.tw-w-full.tw-px-19px.sm\\:tw-px-27px.tw-py-4.tw-border-solid.tw-border-b.tw-border-gray-500 ul > li::text').getall()
        adresse = ' '.join([elem.strip() for elem in adresse_elements if elem.strip()])

        infos = response.css('div.tw-border-solid.tw-border.tw-border-gray-500 .tw-font-medium div::text').getall()

        # Extraction du code du département
        match = re.search(r'(\d{2})\d{3}', adresse)
        code_departement = match.group(1) if match else None

        while len(infos) < 5:
            infos.append(None)

        details = {
            'adresse': adresse,
            'code_departement': code_departement,
            'taux_reussite_bac': infos[0],
            'taux_mentions_bac': infos[1],
            'effectifs_terminale': infos[2],
            'classement_lycees_generaux_technos': infos[3],
            'classement_lycees_pros': infos[4]
        }

        yield {
            **first_box,
            **second_box,
            **details
        }

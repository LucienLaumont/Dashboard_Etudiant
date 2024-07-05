from itemadapter import ItemAdapter
import pymongo

class MongoDBPipeline(object):
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb://mongo:27017/")
        self.db = self.client["Database_Etudiant"]
        self.collection = self.db["lycee"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Nettoyage et conversion des données
        cleaned_item = self.clean_data(item)
        # Insertion de l'item nettoyé dans MongoDB
        self.collection.insert_one(cleaned_item)
        return item
    
    def clean_data(self, item):
        # Appliquer le nettoyage et la conversion ici
        for field in ['nombre_etoiles', 'classement', 'mention', 'taux_reussite_bac', 
                      'taux_mentions_bac', 'classement_lycees_generaux_technos', 
                      'classement_lycees_pros']:
            item[field] = self.clean_and_convert(item.get(field))

        item['specialite'] = self.clean_and_convert(item.get('specialite'), is_specialite=True)
        return item

    def clean_and_convert(self, value, is_specialite=False):
        if value is None or value in ['Non communiqué', 'Non classé']:
            return None
        value = value.replace(',', '.').strip()
        if not is_specialite:
            value = value.replace('%', '').replace('/20', '')
        if is_specialite and value:
            value = value[:-3]

        try:
            return float(value) if not is_specialite else value
        except ValueError:
            return None
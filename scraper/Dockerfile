# Utiliser une image Python officielle
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers de requirements et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code du projet dans le conteneur
COPY . .

# Commande pour exécuter le scraper
CMD ["scrapy", "crawl", "etudiantscraper"]

# Utiliser une image Python officielle
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers de requirements et installer les dépendances
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel Dash s'exécute
EXPOSE 8050

# Commande pour lancer l'application Dash
CMD ["python", "app.py"]


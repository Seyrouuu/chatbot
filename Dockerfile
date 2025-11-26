# Utiliser une image Python officielle comme image parente
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt d'abord pour mieux utiliser le cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet Django dans le conteneur
COPY . .

# Créer le dossier staticfiles
RUN python manage.py collectstatic --noinput

# Exposer le port 8000
EXPOSE 8000

# Commande pour exécuter l'application
CMD ["gunicorn", "chatbot_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
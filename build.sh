#!/bin/bash

# Construire l'image Docker
docker build -t chatbot-django .

# Exécuter le conteneur
docker run -p 8000:8000 chatbot-django
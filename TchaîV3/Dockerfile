#Choix de la version de python utilisée, du label maintainers et de l'emplacement
FROM python:3.8
LABEL maintainer="CCC_Lopes_Peyron"
WORKDIR /app

#Copie des bibliothèques requises de la machine hôte vers le conteneur
COPY requirements.txt .
RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip install -r requirements.txt

ENV FLASK_APP=TchaîV3.py
ENV FLASK_ENV=development

#Copie des fichiers de test
COPY . .

#Préparation du lancement
EXPOSE 5000
CMD [ "flask","run", "-h", "0.0.0.0"]
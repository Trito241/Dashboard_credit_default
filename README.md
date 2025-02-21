# Dashboard_credit_scoring
Projet développé dans le cadre du parcours Data Scientist d'OpenClassrooms en partenariat avec CentralSupélec (RNCP niveau 7)

# Objectif
A partir de l'API préalablement déployée, réaliser un dashboard à destination des chargés d'étude afin qu'ils puissent expliquer à leur client les décisions relatives à leur demande de crédit.

Le dashboard interactif prévoit les éléments suivants :

- visualisation et interprétation du score (proba et comparaison au seuil)
- visualisation des principales informations du client
- comparaison des principales informations du clients vs. ensemble des clients
Ce repository recense les fichiers nécessaires au déploiement du dashboard (dévelopé avec Streamlit) :

- [streamlit_app.py](streamlit_app.py) : fichier python du dashboard
- [requirements.txt](requirements.txt), [Profile](Procfile), [setup.sh](setup.sh) : fichiers indispensables pour le déploiement via Heroku
[lien vers le repository principal de ce projet](https://github.com/Trito241/Credit_default)
[lien vers le repository de l'API](https://github.com/Trito241/Credit_default/blob/main/flask_app.py)

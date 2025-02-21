# Dashboard_credit_scoring
Projet développé dans le cadre du parcours Data Scientist d'OpenClassrooms en partenariat avec CentralSupélec (RNCP niveau 7)

# Objectif
À partir de l'API préalablement déployée, a été réalisé un dashboard à destination des chargés d'étude afin qu'ils puissent expliquer à leur client les décisions relatives à leur demande de crédit.

Le dashboard interactif prévoit les éléments suivants :

- Visualisation et interprétation du score (proba et comparaison au seuil)
- Visualisation des principales informations du client
- Comparaison des principales informations du clients vs. ensemble des clients etc..

Ce repository recense les fichiers nécessaires au déploiement du dashboard sur Heroku (développé avec Streamlit) :

- [Streamlit_app.py](streamlit_app.py) : fichier python du dashboard
- [Requirements.txt](requirements.txt), [Profile](Procfile), [setup.sh](setup.sh) : fichiers indispensables pour le déploiement via Heroku
  
[Lien vers le repository principal de ce projet](https://github.com/Trito241/Credit_default) <br/>
[Lien vers le repository de l'API](https://github.com/Trito241/Credit_default/blob/main/flask_app.py)

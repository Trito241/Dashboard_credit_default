import streamlit as st
import requests
from streamlit.components.v1 import html
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Configuration globale de la page
st.set_page_config(layout="wide", page_title="Prédiction Crédit", page_icon="💳")

# 🎨 **Options d’accessibilité en haut à droite**
col1, col2 = st.columns([2, 1])
with col2:
    with st.expander("🔧 Options d’accessibilité"):
        theme_mode = st.selectbox("Mode d'affichage", ["Clair", "Sombre", "Daltonien"], index=0)
        primary_color = st.color_picker("🎨 Couleur principale", "#4C72B0")
        secondary_color = st.color_picker("🎨 Couleur secondaire", "#E74C3C")
        font_size = st.slider("🔍 Zoom (taille du texte)", 12, 24, 16)

# 🎨 **Appliquer le style CSS selon les options choisies**
custom_css = f"""
    <style>
        html, body, [class*="st"] {{
            font-size: {font_size}px !important;
        }}
        .stApp {{
            background-color: {'#1E1E1E' if theme_mode == 'Sombre' else 'white'};
            color: {'white' if theme_mode == 'Sombre' else 'black'};
        }}
        .stButton>button {{
            background-color: {primary_color} !important;
            color: white !important;
        }}
        .stRadio>div {{
            background-color: {secondary_color} !important;
            color: white !important;
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# URL de l'API Flask qui tourne en local
api_url = "https://credit-default-01-e4556ced9113.herokuapp.com"

# Fonction pour obtenir la liste des clients depuis l'API
def get_client_list():
    response = requests.post(f"{api_url}/id_client")
    if response.status_code == 200:
        data = response.json()
        return data["list_id"]
    else:
        st.error("Erreur lors de la récupération des IDs clients.")
        return []
        
# Fonction pour récupérer les informations personnelles du client
def get_client_info(client_num):
    response = requests.post(f"{api_url}/info_client", json={"client_num": client_num})
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des informations du client {client_num}.")
        return None

# Fonction pour récupérer la jauge d'un client
def get_gauge(client_num):
    response = requests.post(f"{api_url}/gauge", json={"client_num": client_num})
    if response.status_code == 200:
        data = response.json()
        return data["fig"], data["verdict"], data["score"]
    else:
        st.error(f"Erreur lors de la récupération de la jauge pour le client {client_num}.")
        return None, None, None

# Fonction pour récupérer les explications SHAP (Waterfall Plot et Summary Plot)
def get_shap_explanations(client_num):
    response = requests.post(f"{api_url}/explanation", json={"client_num": client_num})
    if response.status_code == 200:
        data = response.json()
        return data["local_explanation"], data["global_explanation"]
    else:
        st.error(f"Erreur lors de la récupération des explications SHAP pour le client {client_num}.")
        return None, None

# Fonction pour récupérer les données de comparaison
def get_comparison_data():
    response = requests.post(f"{api_url}/data_comparaison")
    if response.status_code == 200:
        return response.json()["data"]
    else:
        st.error("Erreur lors de la récupération des données de comparaison.")
        return None

# Interface Streamlit
st.title("Prédiction du défaut de paiement de crédit")

# Récupérer la liste des clients
client_list = get_client_list()

if client_list:
    # Créer la barre latérale pour la sélection de l'ID client
    with st.sidebar:
        st.header("Sélection du client")
        client_num = st.selectbox("Choisissez l'ID du client", client_list, key="client_dropdown")

        # Bouton pour afficher la jauge et les informations personnelles
        if st.button("Afficher la jauge et la décision"):
            gauge_html, verdict, score = get_gauge(client_num)
            st.subheader("📝 Décision et Score")
            st.write(f"**Décision :** {verdict}")
            st.write(f"**Score de probabilité :** {score}")
            # Obtenir la jauge, la décision et le score
            if gauge_html:
                st.subheader("📊 Jauge de décision")
                html(gauge_html, height=500)  # Ajuste la hauteur à ce qui est nécessaire pour l'afficher complètement   
else:
    st.write("Aucun client disponible.")
#-------------------------------------------------------------------------------------------------------------------------------------------
# # 📌 **Section : Positionnement du client par rapport à l’ensemble des clients**
# st.subheader("📊 Positionnement du client par rapport aux autres")

# 🔹 **Récupérer les données**
comparison_data = get_comparison_data()
comparison_data = pd.DataFrame(comparison_data)

if comparison_data is not None:
    comparison_data["SK_ID_CURR"] = comparison_data["SK_ID_CURR"].astype("int")
    
    # Création des onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Informations du client", "📊 Importance des features", "📊 Positionnement du client", "📊 Analyse interactive des variables"])
    
    with tab1:
        st.subheader("📋 Informations du client")
        client_info = get_client_info(client_num)
        if client_info and client_info["status"] == "success":
            st.write(f"**Genre :** {client_info['gender']}")
            st.write(f"**Nombre d'enfants :** {client_info['nb_child']}")
            st.write(f"**Revenu total :** {client_info['income_amount']:.2f} €")
            st.write(f"**Montant du crédit :** {client_info['credit']:.2f} €")
            st.write(f"**Type de revenu :** {client_info['income_type']}")
            st.write(f"**Statut familial :** {client_info['family']}")
    
    with tab2:
        st.subheader("📊 Importance des features")
        
        shap_option = st.selectbox("Sélectionnez le type d'importance des features", ["Importance locale", "Importance globale"])
        
        shap_local_plot, shap_global_plot = get_shap_explanations(client_num)
        
        if shap_option == "Importance locale" and shap_local_plot:
            if shap_local_plot:
                st.image(api_url + shap_local_plot, caption="Waterfall Plot - Importance des features du client")
            else:
                st.warning("Aucune explication locale SHAP disponible.")

        elif shap_option == "Importance globale" and shap_global_plot:
            st.image(api_url + shap_global_plot, caption="Summary Plot - Importance globale")
        else:
            st.warning("Données non disponibles pour cette option.")
    
    with tab3:
        st.subheader("📊 Positionnement du client par rapport aux autres")
        
        # Sélection de la variable à visualiser
        variables = ["EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3", "AMT_CREDIT",
                     "DAYS_EMPLOYED", "CREDIT_TERM", "AMT_INCOME_TOTAL", "AMT_GOODS_PRICE"]
        selected_var = st.selectbox("Sélectionnez une variable à visualiser", variables)
        
        # Vérifier si le client existe dans les données
        client_data = comparison_data[comparison_data["SK_ID_CURR"] == client_num]
        
        if selected_var in comparison_data.columns:
            fig = px.histogram(
                comparison_data,
                x=selected_var,
                nbins=30,
                color_discrete_sequence=["#4C72B0"],
                title=f"Distribution de {selected_var}",
            )
            
            # Ajouter la valeur du client sélectionné en rouge
            if not client_data.empty:
                fig.add_vline(
                    x=client_data[selected_var].values[0], 
                    line_dash="dash",
                    line_color="red", 
                    annotation_text=f"Client N° {client_num}",
                    annotation_position="top"
                )
            
            # fig.update_layout(
            #     xaxis_title=selected_var,
            #     yaxis_title="Nombre de clients",
            #     font=dict(size=14),
            #     title_font=dict(size=16, family="Arial"),
            #     hoverlabel=dict(font_size=14)
            # )
            
            st.plotly_chart(fig, use_container_width=True)
        
    with tab4:
        st.subheader("📊 Analyse interactive des variables")
        
        # Sélection des variables
        cols = comparison_data.columns.tolist()
        var_x = st.selectbox("Sélectionnez la variable X", cols, index=0)
        var_y = st.selectbox("Sélectionnez la variable Y", cols, index=1)
        
        # Détection des types de variables
        is_x_numeric = pd.api.types.is_numeric_dtype(comparison_data[var_x])
        is_y_numeric = pd.api.types.is_numeric_dtype(comparison_data[var_y])
        
        if is_x_numeric and is_y_numeric:
            fig = px.scatter(
                comparison_data,
                x=var_x,
                y=var_y,
                color_discrete_sequence=["#4C72B0"],
                title=f"📈 Relation entre {var_x} et {var_y}",
            )
            
            if not client_data.empty:
                fig.add_trace(px.scatter(
                    x=[client_data[var_x].values[0]],
                    y=[client_data[var_y].values[0]],
                ).data[0])
            
            fig.update_layout(
                font=dict(size=14),
                title_font=dict(size=16, family="Arial"),
                hoverlabel=dict(font_size=14)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Veuillez sélectionner au moins une variable numérique.")


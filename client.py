import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURATION GOOGLE SHEETS ---
import os
# Hadi hya li ghadi t-7elli l-mochkil: kat-jbed l-blassa fin 7at l-code nishan
base_path = os.path.dirname(__file__)
json_path = os.path.join(base_path, "credentials.json")

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# Daba ghadi y-kheddem json_path li fih l-3onwan l-kamel dyal s-sarout
creds = Credentials.from_service_account_file(json_path, scopes=scope)
client = gspread.authorize(creds)


# 7el l-fichier Google Sheets b s-mmiyto
# (T2kd bli s-smiya hya hadik nishan)
SHEET_NAME = "Guide_Demandes"
try:
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    st.error(f"Erreur: Mal9itch l-fichier f Google Drive. T2kd mn s-smiya! {e}")

# --- INTERFACE ---
st.set_page_config(page_title="Inscription - Guide Ghide", page_icon="🎓")

# CSS bach n-ziynou chwiya l-formulaire
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; background-color: #1e3a8a; color: white; border-radius: 10px; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Inscription au Système Guide Ghide")
st.write("3emmer had l-formulaire bach t-sajjal m3ana. L-idara ghadi t-jawbek 9rib!")

with st.form("form_inscription", clear_on_submit=True):
    nom = st.text_input("Smiya w l-Kniya (Nom et Prénom) *")
    tel = st.text_input("Numéro de téléphone *")
    gmail = st.text_input("Gmail (Optionnel)")
    
    st.write("---")
    submit = st.form_submit_button("Sajjalni daba ✅")

if submit:
    if nom.strip() == "" or tel.strip() == "":
        st.error("⚠️ 3afak dkhl smiya w n-nemra dyal t-tilifone!")
    else:
        try:
            # Jib l-waqt dyal daba
            date_daba = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Zid s-ster f Google Sheets
            sheet.append_row([nom, tel, gmail, date_daba])
            
            st.success(f"🎉 Tbarkellah {nom}! Demande dyalk tsiftat b naja7. Tsena l-idara t-contactik.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ W9a3 mochkil mnin bghina n-siftou l-ma3loumat: {e}")


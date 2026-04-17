import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. L-ITTISAL M3A GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # N-jbdou JSON kima howa mn st.secrets bla ma Streamlit y-kherbe9 fih
    creds_dict = json.loads(st.secrets["google_credentials"])
    
    # N-diro l-Ittisal b Google
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # N-7ellou l-fichier Excel
    SHEET_NAME = "Guide_Demandes"
    sheet = client.open(SHEET_NAME).sheet1
    
except Exception as e:
    st.error(f"❌ Mochkil f l-Ittisal b Google wla mal9itch l-fichier f Drive: {e}")
    st.stop()

# --- 2. L-INTERFACE DYAL L-APPLICATION ---
st.set_page_config(page_title="Inscription - Guide Ghide", page_icon="🎓")

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
            date_daba = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([nom, tel, gmail, date_daba])
            st.success(f"🎉 Tbarkellah {nom}! Demande dyalk tsiftat b naja7. Tsena l-idara t-contactik.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ W9a3 mochkil mnin bghina n-siftou l-ma3loumat: {e}")

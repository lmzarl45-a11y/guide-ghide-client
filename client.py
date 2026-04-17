import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURATION GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # 1. N-jbdou l-ma3loumat mn st.secrets
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # 2. Hada howa s-ster s-si7ri li kay-rigel s-sarout 
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    
    # 3. N-diro l-Ittisal m3a Google API
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # 4. N-7ellou l-fichier Excel
    SHEET_NAME = "Guide_Demandes"
    sheet = client.open(SHEET_NAME).sheet1
    
except Exception as e:
    st.error(f"❌ Mochkil f l-Ittisal b Google wla mal9itch l-fichier f Drive: {e}")
    st.stop()

# --- INTERFACE ---
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

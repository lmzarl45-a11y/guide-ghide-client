import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import textwrap

# --- CONFIGURATION GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # N-jbdou JSON mn Secrets
    creds_dict = json.loads(st.secrets["gcp_service_account_json"])
    
    # --- L-7EL N-NIHA2I DYAL S-SAROUT (Bulletproof Fix) ---
    raw_key = creds_dict["private_key"]
    
    # 1. N-7iydou l-hwayej zaydin kamlin bach tb9a ghir chifra n9iya
    body = raw_key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
    body = body.replace(" ", "").replace("\n", "").replace("\\n", "")
    
    # 2. N-3awdou n-bniw s-sarout b t-tari9a li kat-bghiha Google (64 7arf f s-ster)
    proper_body = "\n".join(textwrap.wrap(body, 64))
    proper_key = f"-----BEGIN PRIVATE KEY-----\n{proper_body}\n-----END PRIVATE KEY-----\n"
    
    # 3. N-rj3ou s-sarout l-m9ad l-dictionnaire
    creds_dict["private_key"] = proper_key
    # ------------------------------------------------------
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Mochkil f l'ittisal m3a Google: {e}")
    st.stop()

# 7el l-fichier Google Sheets b s-mmiyto
SHEET_NAME = "Guide_Demandes"
try:
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    st.error(f"❌ Erreur: Mal9itch l-fichier f Google Drive. T2kd mn s-smiya w l-partage! {e}")
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

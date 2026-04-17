import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. L-ITTISAL M3A GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    creds_dict = json.loads(st.secrets["google_credentials"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    SHEET_NAME = "Guide_Demandes"
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    st.error(f"❌ Mochkil f l-Ittisal b Google wla mal9itch l-fichier f Drive: {e}")
    st.stop()

# --- 2. L-INTERFACE (ANIMATIONS + CONFIRMATION) ---
st.set_page_config(page_title="Inscription - Centre ae", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* 1. KHALFIA ANIMÉE */
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)), url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        animation: moveBackground 25s linear infinite alternate;
    }
    @keyframes moveBackground {
        0% { background-position: left bottom; }
        100% { background-position: right top; }
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    /* 2. ANIMATION DYAL DKHLA (FADE IN UP) */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-header { 
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.85) 0%, rgba(212, 175, 55, 0.85) 100%); 
        padding: 40px 20px; 
        border-radius: 15px; 
        text-align: center; 
        color: white; 
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        animation: fadeInUp 0.8s ease-out; /* Dkhla b animation */
    }
    .main-header h1 { font-weight: 800; font-size: 2.2rem; margin-bottom: 10px; }
    .main-header p { font-size: 1.1rem; opacity: 0.9; }

    /* FORMULAIRE M-ANIMI */
    [data-testid="stForm"] {
        background-color: rgba(30, 41, 59, 0.65);
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        animation: fadeInUp 1s ease-out 0.2s both; /* Dkhla m3tla chwiya 3la l-header */
    }

    .stTextInput>div>div>input {
        background-color: rgba(15, 23, 42, 0.7);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 1px #d4af37;
        transform: scale(1.01); /* Animation sghira f l-input */
    }

    /* 3. ANIMATION PULSE L-BOUTONA */
    @keyframes pulseBtn {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }

    .stButton>button { 
        width: 100%; 
        background: linear-gradient(to right, #1e3a8a, #2563eb); 
        color: white; 
        border: none;
        border-radius: 8px; 
        height: 55px; 
        font-size: 1.1rem;
        font-weight: 600; 
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        margin-top: 15px;
        animation: pulseBtn 2s infinite; /* L-Boutona kat-nbed dima */
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #2563eb, #3b82f6);
        transform: translateY(-3px);
        animation: none; /* Kat7bess l-pulse mnin t7et 3liha s-souris */
        box-shadow: 0 10px 20px -3px rgba(37, 99, 235, 0.5);
    }

    .stTextInput label, .stCheckbox label {
        font-weight: 600;
        color: #cbd5e1;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENU DYAL L-PAGE ---
st.markdown('''
    <div class="main-header">
        <h1>🎓 Centre ae - Orientation</h1>
        <p>Portail d'inscription officiel pour l'accompagnement post-bac</p>
    </div>
''', unsafe_allow_html=True)

with st.form("form_inscription", clear_on_submit=True):
    st.write("### 📝 Formulaire d'inscription")
    st.write("Veuillez remplir soigneusement vos informations. L'équipe Guide Ghide vous contactera très prochainement.")
    st.write("") 

    nom = st.text_input("👤 Nom et Prénom (Smiya w l-Kniya) *")
    tel = st.text_input("📱 Numéro de téléphone *")
    gmail = st.text_input("📧 Adresse Email (Gmail) *")
    
    st.write("---")
    # --- L-KHASIYA DYAL T-T2KID (CONFIRMATION) ---
    mt2ked = st.checkbox("✅ Je confirme que mes informations sont correctes (Ana mt2ked mn l-ma3loumat)")
    
    submit = st.form_submit_button("Confirmer l'inscription 🚀")

# Mnin kay-wrek 3la Sifet
if submit:
    # 1. Kay-t2ked wach 3emmer s-smiya w n-nemra
    if nom.strip() == "" or tel.strip() == "":
        st.error("⚠️ 3afak dkhl smiya w n-nemra dyal t-tilifone!")
    # 2. Kay-t2ked wach wrek 3la l-mrbe3 dyal l-Confirmation
    elif not mt2ked:
        st.warning("⚠️ Khassk t-wrek 3la 'Je confirme' (Ana mt2ked) bach t-9der t-sifet t-talab dyalek!")
    # 3. Kolchi s7i7 -> Kay-sifet l-Excel
    else:
        try:
            date_daba = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([nom, tel, gmail, date_daba])
            st.success(f"🎉 Félicitations {nom} ! Votre demande a été envoyée avec succès. L'administration vous contactera bientôt.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ W9a3 mochkil mnin bghina n-siftou l-ma3loumat: {e}")

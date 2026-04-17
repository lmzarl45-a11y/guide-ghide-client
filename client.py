import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- 1. L-ITTISAL M3A GOOGLE SHEETS ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # N-jbdou JSON kima howa mn st.secrets
    creds_dict = json.loads(st.secrets["google_credentials"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    SHEET_NAME = "Guide_Demandes"
    sheet = client.open(SHEET_NAME).sheet1
except Exception as e:
    st.error(f"❌ Mochkil f l-Ittisal b Google wla mal9itch l-fichier f Drive: {e}")
    st.stop()

# --- 2. L-INTERFACE DYAL L-APPLICATION (DESIGN ANIMÉ & PREMIUM) ---
st.set_page_config(page_title="Inscription - Centre ae", page_icon="🎓", layout="centered")

# CSS jdid m3a TSWIRA w ANIMATION (Glassmorphism)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* 1. L-KHALFIA (BACKGROUND) B TSWIRA W ANIMATION */
    .stApp {
        /* Hna drna tswira + wahed l-kholassa zr9a gham9a (overlay) bach l-ktaba tban mzyan */
        background-image: linear-gradient(rgba(15, 23, 42, 0.8), rgba(15, 23, 42, 0.9)), url("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        /* L-Animation smitha moveBackground w kat-t3awed dima */
        animation: moveBackground 25s linear infinite alternate;
    }

    /* 2. L-ANIMATION DYAL TSWIRA (Kat-t7rek chwiya dima) */
    @keyframes moveBackground {
        0% { background-position: left bottom; }
        100% { background-position: right top; }
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    /* L-Fou9aniya (Header) - rddinaha transparent b Glassmorphism */
    .main-header { 
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.85) 0%, rgba(212, 175, 55, 0.85) 100%); 
        padding: 40px 20px; 
        border-radius: 15px; 
        text-align: center; 
        color: white; 
        margin-bottom: 30px;
        backdrop-filter: blur(10px); /* Kay-dbbeb tswira l-lor */
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .main-header h1 { font-weight: 800; font-size: 2.2rem; margin-bottom: 10px; }
    .main-header p { font-size: 1.1rem; opacity: 0.9; }

    /* L-Mrb3 dyal l-formulaire (Transparent b ddel) */
    [data-testid="stForm"] {
        background-color: rgba(30, 41, 59, 0.65); /* Chwiya transparent */
        backdrop-filter: blur(12px); /* Zlaj m-dbbeb */
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* L-Blayes fin kay-khedmo t-talamid (Inputs) */
    .stTextInput>div>div>input {
        background-color: rgba(15, 23, 42, 0.7);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 12px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 0 1px #d4af37;
    }

    /* L-Boutona dyal s-sifet */
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
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #2563eb, #3b82f6);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        border: none;
        color: white;
    }

    .stTextInput label {
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 5px;
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

st.write("### 📝 Formulaire d'inscription")
st.write("Veuillez remplir soigneusement vos informations. L'équipe Guide Ghide vous contactera très prochainement.")
st.write("") 

with st.form("form_inscription", clear_on_submit=True):
    nom = st.text_input("👤 Nom et Prénom (Smiya w l-Kniya) *")
    tel = st.text_input("📱 Numéro de téléphone *")
    gmail = st.text_input("📧 Adresse Email (Gmail) *")
    
    st.write("---")
    submit = st.form_submit_button("Confirmer l'inscription 🚀")

if submit:
    if nom.strip() == "" or tel.strip() == "":
        st.error("⚠️ 3afak dkhl smiya w n-nemra dyal t-tilifone!")
    else:
        try:
            date_daba = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([nom, tel, gmail, date_daba])
            st.success(f"🎉 Félicitations {nom} ! Votre demande a été envoyée avec succès. L'administration vous contactera bientôt.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ W9a3 mochkil mnin bghina n-siftou l-ma3loumat: {e}")

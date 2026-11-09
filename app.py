from datetime import datetime
import streamlit as st

# Configurazione della pagina dell'app
st.set_page_config(
    page_title="Gestione Muffulette e Scorte",
    page_icon="🥖",
    layout="wide",
)

# --- CSS PERSONALIZZATO: COLORI PASTELLO E BOX SQUADRATI ---
st.markdown(
    """
    <style>
        /* Sfondo generale della pagina */
        .stApp {
            background-color: #f9fbfd;
            color: #2c3e50;
        }
        
        /* Box informativi squadrati con tonalità pastello */
        .stAlert {
            border-radius: 0px !important;
            border-left: 6px solid #a8dadc !important;
            background-color: #f1faee !important;
            color: #1d3557 !important;
        }
        
        /* Pulsanti squadrati in stile pastello chiaro */
        .stButton > button {
            border-radius: 0px !important;
            background-color: #e2eafc !important;
            color: #2c3e50 !important;
            border: 1px solid #b6c9f0 !important;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #d0dffb !important;
            border-color: #9ab4ee !important;
        }
        
        /* Pulsante di download report */
        div.stDownloadButton > button {
            background-color: #d8f3dc !important;
            border: 1px solid #b7e4c7 !important;
            color: #1b4332 !important;
        }
        div.stDownloadButton > button:hover {
            background-color: #b7e4c7 !important;
        }
        
        /* Campi di input e form squadrati */
        input {
            border-radius: 0px !important;
        }
        div[data-testid="stForm"] {
            border-radius: 0px !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #ffffff;
            padding: 20px;
        }
        
        /* Intestazioni delle sezioni */
        h1, h2, h3 {
            color: #1e293b;
        }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🥖 Panificio: Gestione Muffulette e Scorte")
st.write(
    "Controllo scorte per variante, inserimento prenotazioni rapido e rubrica"
    " alfabetica."
)

# Inizializzazione dello stato
if "prenotazioni" not in st.session_state:
    st.session_state.prenotazioni = []
if "iniziale_v1" not in st.session_state:
    st.session_state.iniziale_v1 = 50
if "iniziale_v2" not in st.session_state:
    st.session_state.iniziale_v2 = 50
if "banco_v1" not in st.session_state:
    st.session_state.banco_v1 = 0
if "banco_v2" not in st.session_state:
    st.session_state.banco_v2 = 0

st.write("---")

# --- CALCOLI DI MAGAZZINO E CONSEGNE ---
tot_pren_v1 = sum(p["v1"] for p in st.session_state.prenotazioni)
tot_pren_v2 = sum(p["v2"] for p in st.session_state.prenotazioni)

rimasti_v1 = st.session_state.iniziale_v1 - tot_pren_v1
rimasti_v2 = st.session_state.iniziale_v2 - tot_pren_v2

consegnati_v1 = sum(
    p["v1"] for p in st.session_state.prenotazioni if p["evaso"]
)
consegnati_v2 = sum(
    p["v2"] for p in st.session_state.prenotazioni if p["evaso"]
)

ordini_in_attesa = [p for p in st.session_state.prenotazioni if not p["evaso"]]
ordini_evasi = [p for p in st.session_state.prenotazioni if p["evaso"]]

# Conteggio ordini e pezzi relativi per ciascuna variante
ordini_attesa_v1 = sum(1 for p in ordini_in_attesa if p["v1"] > 0)
pezzi_attesa_v1 = sum(p["v1"] for p in ordini_in_attesa if p["v1"] > 0)

ordini_evasi_v1 = sum(1 for p in ordini_evasi if p["v1"] > 0)
pezzi_evasi_v1 = sum(p["v1"] for p in ordini_evasi if p["v1"] > 0)

ordini_attesa_v2 = sum(1 for p in ordini_in_attesa if p["v2"] > 0)
pezzi_attesa_v2 = sum(p["v2"] for p in ordini_in_attesa if p["v2"] > 0)

ordini_evasi_v2 = sum(1 for p in ordini_evasi if p["v2"] > 0)
pezzi_evasi_v2 = sum(p["v2"] for p in ordini_evasi if p["v2"] > 0)


# =====================================================================
# SEZIONE PRINCIPALE AFFIANCATA: GESTIONE SCORTE (SINISTRA) & NUOVA PRENOTAZIONE (DESTRA)
# =====================================================================
col_principale_1, col_principale_2 = st.columns(2, gap="large")

# --- COLONNA SINISTRA: GESTIONE SCORTE E BANCO PER VARIANTE ---
with col_principale_1:
    st.subheader("📦 Gestione Scorte e Banco")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.markdown("### 🌿 Con finocchio")
        st.session_state.iniziale_v1 = st.number_input(
            "Disp. iniziale",
            min_value=0,
            step=1,
            value=st.session_state.iniziale_v1,
            key="num_ini_v1",
        )
        st.session_state.banco_v1 = st.number_input(
            "Venduti al banco",
            min_value=0,
            step=1,
            value=st.session_state.banco_v1,
            key="num_banco_v1",
        )

        st.info(
            f"• Prenotati: **{tot_pren_v1} pz**\n\n"
            f"• Rimasti: **{rimasti_v1} pz**\n\n"
            f"• 📦 **Consegnati:** {consegnati_v1} pz\n"
            f"• ✅ **Ordini evasi:** {ordini_evasi_v1} ({pezzi_evasi_v1} pz)\n"
            f"• ⏳ **Ordini da evadere:** {ordini_attesa_v1} ({pezzi_attesa_v1} pz)"
        )

    with col_v2:
        st.markdown("### 🌾 Senza finocchio")
        st.session_state.iniziale_v2 = st.number_input(
            "Disp. iniziale",
            min_value=0,
            step=1,
            value=st.session_state.iniziale_v2,
            key="num_ini_v2",
        )
        st.session_state.banco_v2 = st.number_input(
            "Venduti al banco",
            min_value=0,
            step=1,
            value=st.session_state.banco_v2,
            key="num_banco_v2",
        )

        st.info(
            f"• Prenotati: **{tot_pren_v2} pz**\n\n"
            f"• Rimasti: **{rimasti_v2} pz**\n\n"
            f"• 📦 **Consegnati:** {consegnati_v2} pz\n"
            f"• ✅ **Ordini evasi:** {ordini_evasi_v2} ({pezzi_evasi_v2} pz)\n"
            f"• ⏳ **Ordini da evadere:** {ordini_attesa_v2} ({pezzi_attesa_v2} pz)"
        )

# --- COLONNA DESTRA: AGGIUNGI NUOVA PRENOTAZIONE ---
with col_principale_2:
    st.subheader("📋 Aggiungi Nuova Prenotazione")

    with st.form("form_prenotazione", clear_on_submit=True):
        nome_cliente = st.text_input("Nome del cliente")
        telefono = st.text_input("Numero di telefono")

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            qta_v1 = st.number_input(
                "Con finocchio (pz)", min_value=0, step=1, value=0
            )
        with col_q2:
            qta_v2 = st.number_input(
                "Senza finocchio (pz)", min_value=0, step=1, value=0
            )

        extra = st.text_input("Altri prodotti extra (opzionale)")

        submitted = st.form_submit_button("Salva Prenotazione")
        if submitted:
            if nome_cliente.strip() == "":
                st.warning("Inserisci almeno il nome del cliente.")
            elif qta_v1 > rimasti_v1 or qta_v2 > rimasti_v2:
                st.error(
                    "❌ Attenzione: Stai tentando di prenotare più pezzi di"
                    " quelli rimasti in magazzino!"
                )
            else:
                st.session_state.prenotazioni.append({
                    "cliente": nome_cliente.strip(),
                    "telefono": telefono if telefono else "Non specificato",
                    "v1": int(qta_v1),
                    "v2": int(qta_v2),
                    "extra": extra if extra else "",
                    "evaso": False,
                })
                st.success(f"Prenotazione salvata per {nome_cliente}!")
                st.rerun()

st.write("---")

# =====================================================================
# SEZIONE 3: RUBRICA ORDINI DA CONSEGNARE (ALFABETICA)
# =====================================================================
if st.session_state.prenotazioni:
    st.subheader(
        f"📝 Ordini in Attesa di Ritiro ({len(ordini_in_attesa)} da evadere)"
    )

    if not ordini_in_attesa:
        st.success(
            "🎉 Ottimo! Tutti gli ordini registrati sono stati ritirati ed"
            " evasi."
        )
    else:
        attesa_ordinati = sorted(
            ordini_in_attesa, key=lambda x: x["cliente"].lower()
        )
        lettera_corrente = ""

        for p in attesa_ordinati:
            prima_lettera = p["
from datetime import datetime
import streamlit as st

# Configurazione della pagina dell'app
st.set_page_config(
    page_title="Gestione Muffulette e Scorte", page_icon="🥖", layout="centered"
)

st.title("🥖 Panificio: Gestione Muffulette e Scorte")
st.write(
    "Controllo scorte, vendite al banco e prenotazioni in ordine alfabetico con spunte."
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

# --- SEZIONE 1: GESTIONE AFFIANCATA PER VARIANTE ---
st.subheader("📦 Gestione Scorte, Banco e Rimanenti")

col_v1, col_v2 = st.columns(2)

# --- COLONNA 1: CON FINOCCHIO ---
with col_v1:
    st.markdown("### 🌿 Con finocchio")
    st.session_state.iniziale_v1 = st.number_input(
        "Disponibilità iniziale",
        min_value=0,
        step=1,
        value=st.session_state.iniziale_v1,
        key="num_ini_v1",
    )
    st.session_state.banco_v1 = st.number_input(
        "Venduti al banco (senza prenotazione)",
        min_value=0,
        step=1,
        value=st.session_state.banco_v1,
        key="num_banco_v1",
    )

    tot_pren_v1 = sum(p["v1"] for p in st.session_state.prenotazioni)
    rimasti_v1 = st.session_state.iniziale_v1 - tot_pren_v1
    tot_distribuito_v1 = tot_pren_v1 + st.session_state.banco_v1

    st.info(
        f"• Prenotati: **{tot_pren_v1} pz**\n\n"
        f"• Rimasti in magazzino: **{rimasti_v1} pz**\n\n"
        f"• **Totale distribuito:** {tot_distribuito_v1} pz"
    )

# --- COLONNA 2: SENZA FINOCCHIO ---
with col_v2:
    st.markdown("### 🌾 Senza finocchio")
    st.session_state.iniziale_v2 = st.number_input(
        "Disponibilità iniziale",
        min_value=0,
        step=1,
        value=st.session_state.iniziale_v2,
        key="num_ini_v2",
    )
    st.session_state.banco_v2 = st.number_input(
        "Venduti al banco (senza prenotazione)",
        min_value=0,
        step=1,
        value=st.session_state.banco_v2,
        key="num_banco_v2",
    )

    tot_pren_v2 = sum(p["v2"] for p in st.session_state.prenotazioni)
    rimasti_v2 = st.session_state.iniziale_v2 - tot_pren_v2
    tot_distribuito_v2 = tot_pren_v2 + st.session_state.banco_v2

    st.info(
        f"• Prenotati: **{tot_pren_v2} pz**\n\n"
        f"• Rimasti in magazzino: **{rimasti_v2} pz**\n\n"
        f"• **Totale distribuito:** {tot_distribuito_v2} pz"
    )

st.write("---")

# --- SEZIONE 2: AGGIUNGI PRENOTAZIONE ---
st.subheader("📋 Aggiungi Nuova Prenotazione")

with st.form("form_prenotazione", clear_on_submit=True):
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        nome_cliente = st.text_input("Nome del cliente")
    with col_c2:
        telefono = st.text_input("Numero di telefono")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        qta_v1 = st.number_input(
            "Con finocchio (pezzi)", min_value=0, step=1, value=0
        )
    with col_q2:
        qta_v2 = st.number_input(
            "Senza finocchio (pezzi)", min_value=0, step=1, value=0
        )

    extra = st.text_input("Altri prodotti extra (es. 2 focacce, opzionale)")

    submitted = st.form_submit_button("Salva Prenotazione")
    if submitted:
        if nome_cliente.strip() == "":
            st.warning("Inserisci almeno il nome del cliente.")
        elif qta_v1 > rimasti_v1 or qta_v2 > rimasti_v2:
            st.error(
                "❌ Attenzione: Stai tentando di prenotare più pezzi di quelli"
                " rimasti in magazzino!"
            )
        else:
            st.session_state.prenotazioni.append({
                "cliente": nome_cliente.strip(),
                "telefono": telefono if telefono else "Non specificato",
                "v1": int(qta_v1),
                "v2": int(qta_v2),
                "extra": extra if extra else "",
                "evaso": False,  # Stato iniziale dell'ordine: non evaso
            })
            st.success(f"Prenotazione salvata per {nome_cliente}!")
            st.rerun()

# --- SEZIONE 3: ELENCO ORDINATO E GESTIONE SPUNTE (EVASI / DA CONSEGNARE) ---
if st.session_state.prenotazioni:
    st.write("---")
    st.subheader("📝 Gestione Ordini e Spunte")

    # Ordina alfabeticamente la lista in base al nome del cliente
    prenotazioni_ordinate = sorted(
        st.session_state.prenotazioni, key=lambda x: x["cliente"].lower()
    )

    # Aggiorna lo stato delle spunte basandosi sui checkbox interattivi
    for p in prenotazioni_ordinate:
        # Creiamo una chiave unica per ogni cliente
        chiave_checkbox = f"evaso_{p['cliente']}"
        # Mostriamo il checkbox con il nome, telefono e quantità
        extra_txt = f" | Extra: {p['extra']}" if p["extra"] else ""
        testo_etichetta = f"**{p['cliente']}** (Tel: {p['telefono']}) ➔ Con finocchio: {p['v1']} | Senza finocchio: {p['v2']}{extra_txt}"

        # Memorizziamo lo stato della spunta dentro l'elemento stesso
        p["evaso"] = st.checkbox(
            testo_etichetta, value=p["evaso"], key=chiave_checkbox
        )

    if st.button("🗑️ Svuota tutte le prenotazioni"):
        st.session_state.prenotazioni = []
        st.rerun()

st.write("---")

# --- SEZIONE 4: DOWNLOAD REPORT ---
data_corrente = datetime.now().strftime("%d-%m-%Y")
orario_corrente = datetime.now().strftime("%H:%M")
nome_file = f"report_muffulette_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

linee_report = [
    "=" * 60,
    "     REPORT GIORNALIERO E SCORTE - MUFFULETTE",
    "=" * 60,
    f"Data: {data_corrente} - Orario: {orario_corrente}\n",
    f"DISPONIBILITÀ INIZIALI: Con finocchio: {st.session_state.iniziale_v1} pz | Senza finocchio: {st.session_state.iniziale_v2} pz\n",
    "📋 ELENCO COMPLETO PRENOTAZIONI (IN ORDINE ALFABETICO):",
]

# Ordiniamo alfabeticamente anche nel file di testo del report
prenotazioni_report = sorted(
    st.session_state.prenotazioni, key=lambda x: x["cliente"].lower()
)

if not prenotazioni_report:
    linee_report.append("   Nessuna prenotazione registrata.")
else:
    for p in prenotazioni_report:
        stato = "[EVASO/RITIRATO]" if p["evaso"] else "[DA CONSEGNARE]"
        extra_testo = f" | Extra: {p['extra']}" if p["extra"] else ""
        linee_report.append(
            f" {stato} {p['cliente']} (Tel: {p['telefono']}): {p['v1']} Con"
            f" finocchio, {p['v2']} Senza finocchio{extra_testo}"
        )

linee_report.extend([
    f"\n📊 RIEPILOGO FINALE - CON FINOCCHIO",
    f"   • Iniziali: {st.session_state.iniziale_v1} | Prenotati: {tot_pren_v1} |"
    f" Banco: {st.session_state.banco_v1}",
    f"   • Rimanenti in magazzino: {rimasti_v1} pz",
    f"   • Totale distribuito: {tot_distribuito_v1} pz",
    f"\n📊 RIEPILOGO FINALE - SENZA FINOCCHIO",
    f"   • Iniziali: {st.session_state.iniziale_v2} | Prenotati: {tot_pren_v2} |"
    f" Banco: {st.session_state.banco_v2}",
    f"   • Rimanenti in magazzino: {rimasti_v2} pz",
    f"   • Totale distribuito: {tot_distribuito_v2} pz",
    "=" * 60,
])

testo_report = "\n".join(linee_report)

st.download_button(
    label="📥 Scarica Report Giornaliero in TXT",
    data=testo_report,
    file_name=nome_file,
    mime="text/plain",
)
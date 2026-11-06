from datetime import datetime
import streamlit as st

# Configurazione della pagina dell'app
st.set_page_config(
    page_title="Gestione Muffulette e Scorte", page_icon="🥖", layout="centered"
)

st.title("🥖 Panificio: Gestione Muffulette e Scorte")
st.write(
    "Controlla le scorte iniziali, scala le prenotazioni e gestisci la produzione."
)

# Inizializzazione della memoria temporanea per le prenotazioni
if "prenotazioni" not in st.session_state:
    st.session_state.prenotazioni = []

# --- SEZIONE 0: IMPOSTAZIONE SCORTE / DISPONIBILITÀ INIZIALE ---
st.subheader("📦 Disponibilità Iniziale (Totale in Laboratorio)")
col_st1, col_st2 = st.columns(2)
with col_st1:
    totale_iniziale_v1 = st.number_input(
        "Totale iniziale 'Con finocchio'", min_value=0, step=1, value=50
    )
with col_st2:
    totale_iniziale_v2 = st.number_input(
        "Totale iniziale 'Senza finocchio'", min_value=0, step=1, value=50
    )

# Calcolo dei totali già prenotati finora
tot_prenotati_v1 = sum(p["v1"] for p in st.session_state.prenotazioni)
tot_prenotati_v2 = sum(p["v2"] for p in st.session_state.prenotazioni)

# Calcolo delle scorte rimanenti
rimanenti_v1 = totale_iniziale_v1 - tot_prenotati_v1
rimanenti_v2 = totale_iniziale_v2 - tot_prenotati_v2

# Mostra un box visivo con le scorte rimanenti in tempo reale
st.info(
    f"🔍 **Scorte Rimanenti Disponibili:**\n\n"
    f"- **Con finocchio:** {rimanenti_v1} pz disponibili (su {totale_iniziale_v1} iniziali)\n"
    f"- **Senza finocchio:** {rimanenti_v2} pz disponibili (su {totale_iniziale_v2} iniziali)"
)

st.write("---")

# --- SEZIONE 1: AGGIUNGI PRENOTAZIONE ---
st.subheader("📋 Aggiungi Nuova Prenotazione")

with st.form("form_prenotazione", clear_on_submit=True):
    nome_cliente = st.text_input("Nome del cliente")
    telefono = st.text_input("Numero di telefono")

    col1, col2 = st.columns(2)
    with col1:
        qta_v1 = st.number_input(
            "Con finocchio (pezzi)", min_value=0, step=1, value=0
        )
    with col2:
        qta_v2 = st.number_input(
            "Senza finocchio (pezzi)", min_value=0, step=1, value=0
        )

    extra = st.text_input("Altri prodotti extra (es. 2 focacce, opzionale)")

    submitted = st.form_submit_button("Salva Prenotazione")
    if submitted:
        if nome_cliente.strip() == "":
            st.warning("Inserisci almeno il nome del cliente.")
        elif qta_v1 > rimanenti_v1 or qta_v2 > rimanenti_v2:
            st.error(
                "❌ Attenzione: Stai tentando di prenotare più pezzi di quelli rimanenti in magazzino!"
            )
        else:
            st.session_state.prenotazioni.append({
                "cliente": nome_cliente,
                "telefono": telefono if telefono else "Non specificato",
                "v1": int(qta_v1),
                "v2": int(qta_v2),
                "extra": extra if extra else "",
            })
            st.success(f"Prenotazione salvata per {nome_cliente}!")
            st.rerun()

# Visualizza l'elenco delle prenotazioni inserite finora
if st.session_state.prenotazioni:
    st.write("---")
    st.subheader("📝 Elenco Prenotazioni di Oggi")
    for i, p in enumerate(st.session_state.prenotazioni, 1):
        extra_txt = f" | Extra: {p['extra']}" if p["extra"] else ""
        st.text(
            f"{i}. {p['cliente']} (Tel: {p['telefono']}) — Con finocchio: {p['v1']}, Senza finocchio: {p['v2']}{extra_txt}"
        )

    if st.button("🗑️ Svuota tutte le prenotazioni"):
        st.session_state.prenotazioni = []
        st.rerun()

st.write("---")

# --- SEZIONE 2: VENDITE LIBERE AL BANCO ---
st.subheader("🛍️ Vendite al Banco (Senza Prenotazione)")
col_v1, col_v2 = st.columns(2)
with col_v1:
    vendite_libere_v1 = st.number_input(
        "Con finocchio venduti al banco", min_value=0, step=1, value=0
    )
with col_v2:
    vendite_libere_v2 = st.number_input(
        "Senza finocchio venduti al banco", min_value=0, step=1, value=0
    )

tot_venduto_v1 = tot_prenotati_v1 + vendite_libere_v1
tot_venduto_v2 = tot_prenotati_v2 + vendite_libere_v2

st.write("---")

# --- SEZIONE 3: REPORT E PRODUZIONE FINALE ---
st.subheader("📊 Riepilogo e Controllo Scorte")

col_rep1, col_rep2 = st.columns(2)
with col_rep1:
    st.markdown("#### Con finocchio")
    st.write(f"• Disponibilità iniziale: {totale_iniziale_v1} pz")
    st.write(f"• Totale prenotati: {tot_prenotati_v1} pz")
    st.write(f"• Venduti al banco: {vendite_libere_v1} pz")
    st.write(f"• **Rimasti in magazzino:** {rimanenti_v1} pz")

with col_rep2:
    st.markdown("#### Senza finocchio")
    st.write(f"• Disponibilità iniziale: {totale_iniziale_v2} pz")
    st.write(f"• Totale prenotati: {tot_prenotati_v2} pz")
    st.write(f"• Venduti al banco: {vendite_libere_v2} pz")
    st.write(f"• **Rimasti in magazzino:** {rimanenti_v2} pz")

# Generazione del file di testo per il download
data_corrente = datetime.now().strftime("%d-%m-%Y")
orario_corrente = datetime.now().strftime("%H:%M")
nome_file = f"report_muffulette_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"

linee_report = [
    "=" * 60,
    "     REPORT GIORNALIERO E SCORTE - MUFFULETTE",
    "=" * 60,
    f"Data: {data_corrente} - Orario: {orario_corrente}\n",
    f"DISPONIBILITÀ INIZIALE: Con finocchio: {totale_iniziale_v1} pz | Senza finocchio: {totale_iniziale_v2} pz\n",
    "📋 ELENCO PRENOTAZIONI NOMINALI E CONTATTI:",
]

if not st.session_state.prenotazioni:
    linee_report.append("   Nessuna prenotazione registrata.")
else:
    for p in st.session_state.prenotazioni:
        extra_testo = f" | Extra: {p['extra']}" if p["extra"] else ""
        linee_report.append(
            f" - {p['cliente']} (Tel: {p['telefono']}): {p['v1']} Con finocchio, {p['v2']} Senza finocchio{extra_testo}"
        )

linee_report.extend([
    f"\n📊 RIEPILOGO FINALE - CON FINOCCHIO",
    f"   • Iniziali: {totale_iniziale_v1} | Prenotati: {tot_prenotati_v1} | Banco: {vendite_libere_v1}",
    f"   • Rimanenti in magazzino: {rimanenti_v1} pz",
    f"\n📊 RIEPILOGO FINALE - SENZA FINOCCHIO",
    f"   • Iniziali: {totale_iniziale_v2} | Prenotati: {tot_prenotati_v2} | Banco: {vendite_libere_v2}",
    f"   • Rimanenti in magazzino: {rimanenti_v2} pz",
    "=" * 60,
])

testo_report = "\n".join(linee_report)

st.download_button(
    label="📥 Scarica Report Giornaliero in TXT",
    data=testo_report,
    file_name=nome_file,
    mime="text/plain",
)
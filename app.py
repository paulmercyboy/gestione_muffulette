from datetime import datetime
import streamlit as st

# Configurazione della pagina dell'app
st.set_page_config(
    page_title="Gestione Muffulette e Scorte", page_icon="🥖", layout="centered"
)

st.title("🥖 Panificio: Gestione Muffulette e Scorte")
st.write(
    "Controllo scorte, rubrica alfabetica, ordini in attesa e totale consegnato."
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
# Totale prenotato totale (indipendentemente dalla spunta, per scalare le scorte iniziali)
tot_pren_v1 = sum(p["v1"] for p in st.session_state.prenotazioni)
tot_pren_v2 = sum(p["v2"] for p in st.session_state.prenotazioni)

rimasti_v1 = st.session_state.iniziale_v1 - tot_pren_v1
rimasti_v2 = st.session_state.iniziale_v2 - tot_pren_v2

# Totale consegnato (somma dei pezzi dei soli ordini con spunta "evaso")
consegnati_v1 = sum(
    p["v1"] for p in st.session_state.prenotazioni if p["evaso"]
)
consegnati_v2 = sum(
    p["v2"] for p in st.session_state.prenotazioni if p["evaso"]
)

# Totale effettivo uscito dal laboratorio = Consegnati ai clienti + Venduti liberi al banco
tot_uscito_v1 = consegnati_v1 + st.session_state.banco_v1
tot_uscito_v2 = consegnati_v2 + st.session_state.banco_v2

# Liste di divisione ordini
ordini_in_attesa = [p for p in st.session_state.prenotazioni if not p["evaso"]]
ordini_evasi = [p for p in st.session_state.prenotazioni if p["evaso"]]


# --- SEZIONE 1: GESTIONE AFFIANCATA PER VARIANTE ---
st.subheader("📦 Gestione Scorte, Banco e Consegnati")

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

    st.info(
        f"• In attesa di ritiro: **{sum(p['v1'] for p in ordini_in_attesa)} pz**\n\n"
        f"• Rimasti in magazzino: **{rimasti_v1} pz**\n\n"
        f"• 📦 **Totale consegnato (evasi):** {consegnati_v1} pz\n"
        f"• 🛒 *Uscita totale (banco+consegnati):* {tot_uscito_v1} pz"
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

    st.info(
        f"• In attesa di ritiro: **{sum(p['v2'] for p in ordini_in_attesa)} pz**\n\n"
        f"• Rimasti in magazzino: **{rimasti_v2} pz**\n\n"
        f"• 📦 **Totale consegnato (evasi):** {consegnati_v2} pz\n"
        f"• 🛒 *Uscita totale (banco+consegnati):* {tot_uscito_v2} pz"
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
                "evaso": False,
            })
            st.success(f"Prenotazione salvata per {nome_cliente}!")
            st.rerun()

# --- SEZIONE 3: RUBRICA ORDINI DA CONSEGNARE (ALFABETICA) ---
if st.session_state.prenotazioni:
    st.write("---")
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
            prima_lettera = p["cliente"][0].upper()

            if prima_lettera != lettera_corrente:
                lettera_corrente = prima_lettera
                st.markdown(f"### 🔠 — {lettera_corrente}")

            chiave_checkbox = f"attesa_{p['cliente']}"
            extra_txt = f" | Extra: {p['extra']}" if p["extra"] else ""
            testo_etichetta = (
                f"**{p['cliente']}** (Tel: {p['telefono']}) ➔ Con finocchio:"
                f" {p['v1']} | Senza finocchio: {p['v2']}{extra_txt}"
            )

            spuntato = st.checkbox(
                testo_etichetta, value=False, key=chiave_checkbox
            )
            if spuntato:
                p["evaso"] = True
                st.rerun()

    if ordini_evasi:
        with st.expander(
            f"✅ Visualizza ordini già ritirati / evasi ({len(ordini_evasi)})"
        ):
            for p in ordini_evasi:
                extra_txt = f" | Extra: {p['extra']}" if p["extra"] else ""
                col_ed1, col_ed2 = st.columns([4, 1])
                with col_ed1:
                    st.text(
                        f"✓ {p['cliente']} — Con: {p['v1']} | Senza: {p['v2']}{extra_txt}"
                    )
                with col_ed2:
                    if st.button("Annulla", key=f"Annulla_{p['cliente']}"):
                        p["evaso"] = False
                        st.rerun()

    st.write("")
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
    "📋 ELENCO COMPLETO PRENOTAZIONI:",
]

prenotazioni_report = sorted(
    st.session_state.prenotazioni, key=lambda x: x["cliente"].lower()
)

if not prenotazioni_report:
    linee_report.append("   Nessuna prenotazione registrata.")
else:
    for idx, p in enumerate(prenotazioni_report, 1):
        stato = "[EVASO/RITIRATO]" if p["evaso"] else "[DA CONSEGNARE]"
        extra_testo = f" | Extra: {p['extra']}" if p["extra"] else ""
        linee_report.append(
            f" #{idx} {stato} {p['cliente']} (Tel: {p['telefono']}): {p['v1']}"
            f" Con finocchio, {p['v2']} Senza finocchio{extra_testo}"
        )

linee_report.extend([
    f"\n📊 RIEPILOGO FINALE - CON FINOCCHIO",
    f"   • Iniziali: {st.session_state.iniziale_v1} | Banco: {st.session_state.banco_v1}",
    f"   • Consegnati (ordini evasi): {consegnati_v1} pz",
    f"   • Rimasti in magazzino: {rimasti_v1} pz",
    f"   • Uscita totale magazzino: {tot_uscito_v1} pz",
    f"\n📊 RIEPILOGO FINALE - SENZA FINOCCHIO",
    f"   • Iniziali: {st.session_state.iniziale_v2} | Banco: {st.session_state.banco_v2}",
    f"   • Consegnati (ordini evasi): {consegnati_v2} pz",
    f"   • Rimasti in magazzino: {rimasti_v2} pz",
    f"   • Uscita totale magazzino: {tot_uscito_v2} pz",
    "=" * 60,
])

testo_report = "\n".join(linee_report)

st.download_button(
    label="📥 Scarica Report Giornaliero in TXT",
    data=testo_report,
    file_name=nome_file,
    mime="text/plain",
)
import streamlit as st

# Variabili globali per esempio, in un'app reale dovresti usare un database
spese = []
debiti = {}


# Funzione per aggiungere una spesa
def aggiungi_spesa(descrizione, importo, pagante, partecipanti):
    spesa = {
        'descrizione': descrizione,
        'importo': importo,
        'pagante': pagante,
        'partecipanti': partecipanti
    }
    spese.append(spesa)

    # Calcola la parte di ciascun partecipante
    importo_per_persona = importo / len(partecipanti)
    for persona in partecipanti:
        if persona != pagante:
            if persona not in debiti:
                debiti[persona] = 0
            debiti[persona] += importo_per_persona


# Funzione per saldare un debito
def salda_debito(persona, pagamento):
    if persona in debiti:
        debiti[persona] -= pagamento
        if debiti[persona] <= 0:
            debiti[persona] = 0  # Debito saldato


# Interfaccia utente
st.title("Gestione Spese Condivise")

# Aggiunta di una nuova spesa
st.header("Aggiungi una Spesa")
descrizione = st.text_input("Descrizione della spesa")
importo = st.number_input("Importo", min_value=0.01, step=0.01)
data = st.date_input("Data")
pagante = st.text_input("Chi ha pagato?")
partecipanti_input = st.text_input("Chi ha partecipato? (separa i nomi con una virgola)")

if st.button("Aggiungi Spesa"):
    if descrizione and importo > 0 and pagante and partecipanti_input:
        partecipanti = [persona.strip() for persona in partecipanti_input.split(',')]
        if pagante in partecipanti:
            aggiungi_spesa(descrizione, importo, pagante, partecipanti)
            st.success("Spesa aggiunta con successo!")
        else:
            st.warning(f"{pagante} deve essere nella lista dei partecipanti!")

# Visualizzazione delle spese
st.header("Spese Registrate")
if spese:
    for spesa in spese:
        st.write(f"{spesa['descrizione']} - {spesa['importo']} EUR - Pagato da {spesa['pagante']} il {data}")
else:
    st.write("Nessuna spesa registrata.")

# Visualizzazione debiti
st.header("Debiti Non Saldati")
if debiti:
    for persona, debito in debiti.items():
        st.write(f"{persona} deve {debito} EUR")
else:
    st.write("Nessun debito non saldato.")

# Seleziona il debito da saldare
debito_da_saldare = st.selectbox("Seleziona la persona che ha saldato il debito", list(debiti.keys()))

if debito_da_saldare:
    pagamento = st.number_input("Importo da saldare", min_value=0.01, step=0.01)

    if st.button(f"Saldare debito di {debito_da_saldare}"):
        if pagamento > 0:
            salda_debito(debito_da_saldare, pagamento)
            st.success(f"Debito di {debito_da_saldare} saldato di {pagamento} EUR!")
        else:
            st.warning("Inserisci un importo valido.")

# Visualizzare i debiti aggiornati
st.header("Saldi Aggiornati")
if debiti:
    for persona, debito in debiti.items():
        st.write(f"{persona} deve ancora {debito} EUR")
else:
    st.write("Tutti i debiti sono stati saldati!")

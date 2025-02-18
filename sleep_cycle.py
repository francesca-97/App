import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caricamento del dataset
def load_data():
    file_path = "sleep_cycle_productivity.csv"  # Nome del file caricato
    data = pd.read_csv(file_path)
    # Conversione colonne numeriche dove necessario
    data['Sleep Start Time'] = pd.to_numeric(data['Sleep Start Time'], errors='coerce')
    data['Sleep End Time'] = pd.to_numeric(data['Sleep End Time'], errors='coerce')
    return data

data = load_data()

# Titolo e descrizione dell'app
st.title("🌙 Analisi delle Abitudini del Sonno e Benessere 💤")
st.markdown("""
Questa applicazione analizza le abitudini del sonno e il loro impatto su produttività, umore e livelli di stress. Esplora i dati per individuare correlazioni tra fattori dello stile di vita e qualità del sonno.
""")

# Esplorazione del dataset
st.header("🔍 Esplorazione del Dataset")
st.markdown("""
In questa sezione puoi visualizzare i primi record del dataset o esplorare le statistiche descrittive per avere un'idea generale dei dati analizzati.
""")
if st.checkbox("📄 Mostra i primi 5 record"):
    st.write(data.head())

if st.checkbox("📊 Mostra statistiche descrittive"):
    st.write(data.describe())

# Filtri per esplorazione
st.header("🎯 Filtri Personalizzati")
st.markdown("""
Utilizza i filtri per analizzare un sottoinsieme specifico del dataset in base a genere e fascia d'età. Puoi selezionare il genere e un intervallo di età per affinare l'analisi.
""")

genere = st.selectbox("👤 Seleziona il Genere", options=data['Gender'].unique())
età = st.slider("📅 Seleziona un intervallo di Età", int(data['Age'].min()), int(data['Age'].max()), (20, 40))

filtered_data = data[(data['Gender'] == genere) & (data['Age'].between(età[0], età[1]))]
st.write(filtered_data)

# Suggerimenti per migliorare la qualità del sonno
st.header("💡 Suggerimenti per Migliorare la Qualità del Sonno")
st.markdown("""
Ecco alcuni suggerimenti per migliorare la qualità del sonno:
- **Esercizio fisico**: Un'attività fisica regolare può migliorare la qualità del sonno.
- **Limitare la caffeina**: Ridurre l'assunzione di caffeina, soprattutto nelle ore serali, può favorire un sonno migliore.
- **Tempo davanti allo schermo**: Cerca di limitare il tempo trascorso davanti allo schermo prima di andare a letto per migliorare la qualità del sonno.
""")

# Visualizzazioni interattive
st.header("📈 Visualizzazioni Interattive")
st.markdown("""
Qui puoi esplorare graficamente le relazioni tra diversi fattori legati al sonno, come la qualità, la durata e altri elementi dello stile di vita. Scegli uno dei grafici per visualizzare meglio i dati e le correlazioni.
""")

# Distribuzione della qualità del sonno
if st.checkbox("🌟 Distribuzione della Qualità del Sonno"):
    st.markdown("""
    Questo istogramma mostra come la qualità del sonno è distribuita tra gli utenti, valutata su una scala da 1 (scarsa) a 10 (eccellente).
    La linea di densità aiuta a vedere se la qualità del sonno è generalmente alta o bassa.
    """)
    fig, ax = plt.subplots()
    sns.histplot(data['Sleep Quality'], kde=True, bins=10, ax=ax)
    ax.set_title("Distribuzione della Qualità del Sonno")
    st.pyplot(fig)

# Correlazioni generali
if st.checkbox("🔗 Mappa di Correlazione"):
    st.markdown("""
    La mappa di correlazione evidenzia le relazioni tra tutte le variabili numeriche presenti nel dataset. Valori più vicini a 1 o -1 indicano una forte correlazione positiva o negativa.
    Le celle più scure indicano una correlazion più forte.
    """)
    fig, ax = plt.subplots(figsize=(10, 8))
    correlation = data.select_dtypes(include=['float64', 'int64']).corr()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Mappa di Correlazione")
    st.pyplot(fig)

# Analisi delle ore di lavoro sul sonno
if st.checkbox("💼 Impatto delle Ore di Lavoro sul Sonno"):
    st.markdown("""
    Questo grafico esplora come le ore di lavoro giornaliere possano influire sulla durata e qualità del sonno.
     Un aumento delle ore di lavoro potrebbe ridurre la durata del sonno.
    """)
    fig, ax = plt.subplots()
    sns.scatterplot(x=data['Work Hours (hrs/day)'], y=data['Total Sleep Hours'], ax=ax)
    ax.set_title("Ore di Lavoro vs Ore di Sonno")
    st.pyplot(fig)

# 2. Ore di sonno media per fascia di età
if st.checkbox("⏰ Ore di Sonno Media per Fascia di Età", key="ore_media_fascia_eta"):
    st.markdown("""
    Questo grafico a barre mostra la media delle ore di sonno per fascia d'età.
    """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sleep_by_age = data.groupby('Age')['Total Sleep Hours'].mean()
    sleep_by_age.plot(kind='bar', ax=ax, color='salmon')
    ax.set_title("Ore di Sonno Media per Fascia di Età")
    ax.set_xlabel('Fascia d\'Età')
    ax.set_ylabel('Ore di Sonno Media')
    st.pyplot(fig)

# 3. Correlazione tra qualità del sonno e produttività
if st.checkbox("📈 Correlazione tra Qualità del Sonno e Produttività", key="correlazione_produttivita"):
    st.markdown("""
    Questo boxplot mostra come varia la produttività in base alla qualità del sonno.
    """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=data['Sleep Quality'], y=data['Productivity Score'], ax=ax, color='lightgreen')
    ax.set_title("Produttività vs Qualità del Sonno")
    ax.set_xlabel('Qualità del Sonno')
    ax.set_ylabel('Punteggio di Produttività')
    st.pyplot(fig)

# 4. Distribuzione dell'umore in base alla qualità del sonno
if st.checkbox("🌈 Distribuzione dell'Umore in base alla Qualità del Sonno", key="distribuzione_umore"):
    st.markdown("""
    Questo grafico a scatola (boxplot) mostra come l'umore varia in base alla qualità del sonno.
    """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(x=data['Sleep Quality'], y=data['Mood Score'], ax=ax, color='lightblue')
    ax.set_title("Distribuzione dell'Umore in base alla Qualità del Sonno")
    ax.set_xlabel('Qualità del Sonno')
    ax.set_ylabel('Punteggio dell\'Umore')
    st.pyplot(fig)

# 5. Media delle ore di sonno in base al genere
if st.checkbox("👤 Ore di Sonno Media per Genere", key="ore_media_genere"):
    st.markdown("""
    Questo grafico a barre mostra le ore di sonno medie per genere.
    """)
    fig, ax = plt.subplots(figsize=(8, 6))
    sleep_by_gender = data.groupby('Gender')['Total Sleep Hours'].mean()
    sleep_by_gender.plot(kind='bar', ax=ax, color='orange')
    ax.set_title("Ore di Sonno Media per Genere")
    ax.set_xlabel('Genere')
    ax.set_ylabel('Ore di Sonno Media')
    st.pyplot(fig)

st.markdown("App sviluppata con ❤️ usando Streamlit! 🚀")

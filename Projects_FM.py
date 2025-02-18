import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Funzione per caricare i dati
def load_data():
    return pd.read_csv('target_vaccinati_sicilia_Isemestre2021.csv')

def load_data_sleep():
    file_path = "sleep_cycle_productivity.csv"
    data = pd.read_csv(file_path)
    data['Sleep Start Time'] = pd.to_numeric(data['Sleep Start Time'], errors='coerce')
    data['Sleep End Time'] = pd.to_numeric(data['Sleep End Time'], errors='coerce')
    return data

st.sidebar.header("Benvenuto!👋 Qui puoi esplorare i miei progetti")

project = st.sidebar.selectbox("Scegli il progetto", ["Progetto Vaccinazioni", "Progetto Sonno e Produttività"])


# Carica il progetto selezionato
if project == "Progetto Vaccinazioni":
    st.markdown("### 📊 Analisi delle Vaccinazioni in Sicilia (Primo Semestre 2021)")

    # Descrizione introduttiva
    st.markdown("""Questa tabella esplora i dati relativi alle vaccinazioni del primo semestre 2021 in regione Sicilia. 🏥 
    Seleziona le opzioni per esplorare meglio i dati e visualizzare statistiche e grafici interattivi! 📈""")

    # Mostra i dati
    df = load_data()
    st.write("📝 **Dati delle vaccinazioni**: Qui puoi visualizzare il dataset con tutte le informazioni relative alle vaccinazioni.")
    st.write(df)

    # Statistiche sui vaccinati
    st.markdown("### 📊 Statistiche sui Vaccinati")
    st.markdown("📈 **Statistiche sui vaccinati**: Qui puoi vedere il totale e la media dei vaccinati in Sicilia.")
    totale_vaccinati = df['Vaccinati'].sum()
    media_vaccinati = df['Vaccinati'].mean()
    st.write(f"🧑‍🤝‍🧑 **Totale vaccinati in Sicilia:** {totale_vaccinati}")
    st.write(f"📊 **Media vaccinati per comune:** {media_vaccinati:.2f}")


    # Filtro per provincia
    st.markdown("### 🔍 Filtro per Provincia")
    st.markdown("🎯 **Filtro per Provincia**: Seleziona una provincia per visualizzare i dati relativi alle vaccinazioni specifiche per quella provincia.")
    provincia = st.selectbox("Seleziona la Provincia", df['provincia'].unique())
    df_filtered = df[df['provincia'] == provincia]
    st.write("🔍 **Dati filtrati per provincia selezionata**: Questi sono i dati delle vaccinazioni per la provincia scelta.")
    st.write(df_filtered)

    # Grafico numero vaccinati per classe di età e provincia
    st.markdown("### 📊 Numero di Vaccinati per Classe di Età e Provincia")

    st.markdown("📈 **Grafico delle vaccinazioni per classe di età e provincia**: Qui puoi vedere come il numero di vaccinati varia in base alla classe di età e alla provincia.")
    vaccinati_per_classe_età = df.groupby(['provincia', 'classeEta'])['Vaccinati'].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    vaccinati_per_classe_età.plot(kind='bar', ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Provincia')
    ax.set_title('Numero di Vaccinati per Classe di Età e Provincia')
    st.pyplot(fig)

    # Vaccinazioni per comune
    st.markdown("### 🌍 Vaccinazioni per Comune")
    st.markdown("🏘️ **Vaccinazioni per Comune**: Puoi esplorare i dati di vaccinazione per ciascun comune della Sicilia e filtrare i comuni con un numero specifico di vaccinati.")
    vaccinazioni_comune = df.groupby('Comune')['Vaccinati'].sum()
    soglia = st.slider('📏 Seleziona la soglia di vaccinazioni', 0, int(vaccinazioni_comune.max()), 1000)
    comuni_filtrati = vaccinazioni_comune[vaccinazioni_comune > soglia]
    st.write(f"🗺️ **Comuni con più di {soglia} vaccinati**: Questi sono i comuni con un numero di vaccinati superiore alla soglia selezionata.")
    st.write(comuni_filtrati)

    # Grafico per comuni con più vaccinati
    if not comuni_filtrati.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        comuni_filtrati.plot(kind='bar', ax=ax)
        ax.set_ylabel('Numero di Vaccinati')
        ax.set_xlabel('Comune')
        ax.set_title(f'Comuni con più di {soglia} Vaccinati')
        st.pyplot(fig)
    else:
        st.warning(f"⚠️ Non ci sono comuni con più di {soglia} vaccinati.")

    # Analisi delle vaccinazioni per classe di età
    st.markdown("### 👶 Vaccinazioni per Classe di Età")
    st.markdown("👶 **Vaccinazioni per classe di età**: Visualizza il totale delle vaccinazioni suddivise per classe di età.")
    classe_eta = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
    st.bar_chart(classe_eta.set_index('classeEta'))

    # Analisi delle vaccinazioni per provincia
    st.markdown("### 🏙️ Vaccinazioni per Provincia")
    st.markdown("🏙️ **Vaccinazioni per provincia**: Visualizza il totale delle vaccinazioni per ciascuna provincia della Sicilia.")
    provincia = df.groupby('provincia')['Vaccinati'].sum().reset_index()
    st.bar_chart(provincia.set_index('provincia'))

    # Analisi dell'efficacia delle vaccinazioni
    st.markdown("### 💉 Analisi dell'efficacia delle Vaccinazioni")
    st.markdown("📉 **Efficacia delle vaccinazioni**: Analizza la percentuale di vaccinati per ciascuna classe di età.")
    efficacia = df.groupby('classeEta')['Vaccinati'].sum().reset_index()
    efficacia['percentuale_vaccinati'] = (efficacia['Vaccinati'] / df['Vaccinati'].sum()) * 100
    st.line_chart(efficacia.set_index('classeEta')['percentuale_vaccinati'])

    # Selezione dell'intervallo di tempo
    st.markdown("### 🗓️ Analisi per Intervallo di Tempo")
    st.markdown("⏰ **Selezione intervallo di tempo**: Usa il selettore di date per analizzare i dati delle vaccinazioni in un periodo specifico.")
    inizio = st.date_input("Seleziona la data di inizio:", pd.to_datetime(df['inizioIntervallo']).min())
    fine = st.date_input("Seleziona la data di fine:", pd.to_datetime(df['fineIntervallo']).max())

    # colonne di data  in formato datetime
    df['inizioIntervallo'] = pd.to_datetime(df['inizioIntervallo'])
    df['fineIntervallo'] = pd.to_datetime(df['fineIntervallo'])

    # Converte le date selezionate in datetime
    inizio = pd.to_datetime(inizio)
    fine = pd.to_datetime(fine)

    # Filtro per intervallo di tempo
    df_filtered = df[(df['inizioIntervallo'] >= inizio) & (df['fineIntervallo'] <= fine)]
    st.write(df_filtered)

    # Top 10 province con più vaccinati
    st.markdown("### 🏆 Top 10 Province con Più Vaccinazioni")
    st.markdown("🌟 **Le province con più vaccinazioni**: Questo grafico mostra le 10 province con il maggior numero di vaccinazioni.")
    vaccinazioni_per_provincia = df.groupby('provincia')['Vaccinati'].sum()
    top_province = vaccinazioni_per_provincia.nlargest(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_province.plot(kind='bar', ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Provincia')
    ax.set_title('Top 10 Province con Più Vaccinazioni')
    st.pyplot(fig)


    # Grafico a barre impilate per classe di età
    st.markdown("### 📊 Vaccinazioni per Classe di Età (Stacked)")
    st.markdown("📊 **Grafico a barre impilate**: Questo grafico mostra la distribuzione delle vaccinazioni per classe di età.")
    fig, ax = plt.subplots(figsize=(10, 6))
    vaccinati_per_classe_età.plot(kind='bar', stacked=True, ax=ax)
    ax.set_ylabel('Numero di Vaccinati')
    ax.set_xlabel('Classe di Età')
    ax.set_title('Vaccinazioni per Classe di Età (Distribuzione Stacked)')
    st.pyplot(fig)

    # Esportazione dei dati
    st.markdown("### 📥 Esporta Dati Filtrati")
    st.markdown("💾 **Esporta i dati filtrati**: Puoi esportare i dati filtrati in un file CSV per analisi future.")
    if st.button("🚀 Esporta Dati Filtrati"):
        df_filtered.to_csv("dati_filtrati.csv", index=False)
        st.success("✅ File esportato come 'dati_filtrati.csv'")



elif project == "Progetto Sonno e Produttività":

    data = load_data_sleep()

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

    # Ore di sonno media per fascia di età
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

    #  Correlazione tra qualità del sonno e produttività
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

    # Distribuzione dell'umore in base alla qualità del sonno
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

    # Media delle ore di sonno in base al genere
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



st.markdown("\n❤️ App sviluppata usando Streamlit! 🚀")

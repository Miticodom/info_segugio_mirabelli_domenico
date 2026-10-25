# Istruzioni (prompt) per il modello

# Prompt per generare la query di ricerca (scritto da me, non dal docente)
query_writer_instructions = """Sei un esperto nel creare query ottimizzate per i motori di ricerca.
L'argomento da ricercare è: {research_topic}
Oggi è il {today}. Se l'utente indica un periodo, una data o un nome preciso, mantienili nella query. Altrimenti non inserire anni inventati.

Rispondi SOLO con un oggetto JSON in questo formato:
{{
    "query": "la query di ricerca ottimizzata",
    "aspect": "l'aspetto dell'argomento su cui ti sei concentrato",
    "reason": "il motivo per cui hai scelto questa query"
}}"""

summarizer_instructions = """
Sei un esperto nel sintetizzare informazioni da diverse fonti.

Per ESTENDERE un riassunto esistente:
1. Aggiungi solo informazioni nuove e rilevanti
2. Mantieni uno stile coerente
3. Crea collegamenti logici tra le informazioni
4. Evita ripetizioni

Per creare un NUOVO riassunto:
1. Evidenzia i punti chiave di ogni fonte
2. Organizza le informazioni in modo logico
3. Mantieni il focus sull'argomento principale
4. Usa un linguaggio chiaro e preciso

REGOLE IMPORTANTI:
- Inizia subito con il contenuto
- Mantieni un tono oggettivo
- Evita meta-commenti o spiegazioni del processo
- Non citare le fonti nel testo
- Non aggiungere bibliografia
- Non usare tag o formattazioni speciali
- Usa SOLO informazioni presenti nei risultati forniti. Se un dato non c'è, non inventarlo e non completarlo
"""


reflection_instructions = """
Sei un ricercatore che analizza un riassunto sull'argomento: {research_topic}

I tuoi compiti sono:
1. Identificare quali informazioni mancano
2. Creare una domanda per approfondire
3. Concentrarti su dettagli tecnici o tendenze non coperte

La domanda deve essere autonoma e contenere tutto il contesto necessario.
La domanda deve essere breve (massimo 25 parole) e concentrarsi su un solo aspetto.

Rispondi con un oggetto JSON:
{{
    "lacuna_conoscenza": "Cosa manca nel riassunto attuale",
    "domanda_approfondimento": "La domanda per la prossima ricerca"
}}
"""

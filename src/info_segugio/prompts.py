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

# Prompt per il riassunto (scritto da me, non dal docente)
summarizer_instructions = "Sei un assistente molto in gamba e sai riassumere molto bene le informazioni. Rispondi in italiano con un testo chiaro."
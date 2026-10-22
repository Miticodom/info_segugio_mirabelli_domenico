import json
from datetime import date
import chainlit as cl
from openai import OpenAI
from tavily import TavilyClient
from config import Config
from prompts import query_writer_instructions, summarizer_instructions
from prompts import query_writer_instructions, summarizer_instructions, reflection_instructions


# Inizializzazione del client OpenAI con le configurazioni
client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)

# Funzione per interagire con l'AI
def llm(developer_prompt, user_prompt, temperature=0, response_format={"type": "json_object"}):
    params = {
        "model": Config.LLM_MODEL_LOW,
        "messages": [
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }
    # Il formato (per esempio JSON) si aggiunge solo se richiesto
    if response_format is not None:
        params["response_format"] = response_format
    response = client.chat.completions.create(**params)
    return response.choices[0].message.content 


# Genera una query ottimizzata per la ricerca web
def optimize_search_query(research_topic):
    today = date.today().strftime("%Y-%m-%d")
    formatted_instructions = query_writer_instructions.format(research_topic=research_topic, today=today)
    result = llm(formatted_instructions, "Genera una query per la ricerca web:")
    obj = json.loads(result)
    return obj

def _format_content(result):
    return f"""
Fonte {result['title']}:\n===\n
URL: {result['url']}\n===\n
Contenuto piu' rilevante: {result['content']}\n===\n
"""



# Esegue la ricerca web con Tavily 
def web_research(search_query):
    max_results = 5
    include_raw = False

    tavily_client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    response = tavily_client.search(
        query=search_query,
        max_results=max_results,
        include_raw_content=include_raw,
    )
    results = response.get("results", [])
    titles = [result["title"] for result in results]
    contents = [_format_content(result) for result in results]
    print(titles)
    return {
        "sources_gathered": titles,
        "web_research_results": contents,
    }

# Sintetizza i risultati della ricerca in un riassunto coerente
def summarize_sources(web_research_results, research_topic, running_summary=None):
    current_results = web_research_results[-1]

    if running_summary:
        message = (
            f"Estendi questo riassunto: {running_summary}\n\n"
            f"Con questi nuovi risultati: {current_results} "
            f"Sul tema: {research_topic}"
        )
    else:
        message = (
            f"Genera un riassunto di questi risultati: {current_results} "
            f"Sul tema: {research_topic}"
        )

    output_formatter = None  # Vogliamo del testo semplice
    return llm(summarizer_instructions, message, 0.2, output_formatter)

 # Analizza il riassunto corrente e genera una domanda di approfondimento
def reflect_on_summary(research_topic, running_summary):
    result = llm(
        reflection_instructions.format(research_topic=research_topic),
        f"Identifica una lacuna e genera una domanda per la prossima ricerca basandoti su: {running_summary}",
    )
    return json.loads(result)

@cl.on_message
async def main(message: cl.Message):
    # Fase 1: Generazione della query iniziale
    user_message = message.content
    osq = optimize_search_query(user_message)

    # feedback per l'utente
    query, aspect, reason = osq["query"], osq["aspect"], osq["reason"]
    await cl.Message(
        author="system_assistant",
        content=f"Query di ricerca ottimizzata:\n {query}.\n Mi sono soffermato su questo aspetto:\n {aspect}.\n Per questo motivo:\n {reason}.\n",
    ).send()

    running_summary = None # Inizializza il riassunto corrente come None


    # Esegui la ricerca web
    results = web_research(query)

    # feedback per l'utente
    sources = results["sources_gathered"]
    first_source = sources[0] if sources else "nessuna fonte trovata"
    await cl.Message(
        author="system_assistant",
        content=f"Fonti trovate: {first_source}",
    ).send()

         # Genera o aggiorna il riassunto
    web_research_results = [results["web_research_results"]]  # una lista: un elemento per ogni ricerca
    summary = summarize_sources(web_research_results, query, running_summary)

    # feedback per l'utente
    await cl.Message(
        author="system_assistant",
        content=f"Riassunto attuale: {summary}",
    ).send()

    
    # Genera la prossima query di approfondimento
    ros = reflect_on_summary(query, summary)
    query = ros.get("domanda_approfondimento", f"Dimmi di più su {query}")
    lacuna_conoscenza = ros.get("lacuna_conoscenza", "")

    # feedback per l'utente
    await cl.Message(
        author="system_assistant",
        content=f"Prossima ricerca:\n {query}.\n Mi sono soffermato su questo perché:\n {lacuna_conoscenza}",
    ).send()
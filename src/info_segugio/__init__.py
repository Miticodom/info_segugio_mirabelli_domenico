import json

import chainlit as cl
from openai import OpenAI
from config import Config


# Inizializzazione del client OpenAI con le configurazioni
client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)


# Istruzioni (prompt) per generare la query di ricerca (scritte da me, non dal docente)
query_writer_instructions = """Sei un esperto nel creare query ottimizzate per i motori di ricerca.
L'argomento da ricercare è: {research_topic}

Rispondi SOLO con un oggetto JSON in questo formato:
{{
    "query": "la query di ricerca ottimizzata",
    "aspect": "l'aspetto dell'argomento su cui ti sei concentrato",
    "reason": "il motivo per cui hai scelto questa query"
}}"""


# Funzione per interagire con l'AI
def llm(developer_prompt, user_prompt, temperature=0, response_format={"type": "json_object"}):
    response = client.chat.completions.create(
        model=Config.LLM_MODEL_LOW,
        messages=[
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format=response_format,
    )
    return response.choices[0].message.content


# Genera una query ottimizzata per la ricerca web
def optimize_search_query(research_topic):
    formatted_instructions = query_writer_instructions.format(research_topic=research_topic)
    result = llm(formatted_instructions, "Genera una query per la ricerca web:")
    obj = json.loads(result)
    return obj


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
    
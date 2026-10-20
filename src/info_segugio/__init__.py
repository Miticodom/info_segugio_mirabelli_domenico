import chainlit as cl
from openai import OpenAI
from config import Config


# Inizializzazione del client OpenAI con le configurazioni
client = OpenAI(base_url=Config.AI_API_URL, api_key=Config.AI_API_KEY)


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Echo: {message.content}",
    ).send()
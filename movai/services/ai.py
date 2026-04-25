import cohere
from flask import current_app


def get_cohere_client():
    return cohere.Client(current_app.config["COHERE_API_KEY"])


def get_cohere_response(prompt):
    co = get_cohere_client()
    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.7,
        max_tokens=450,
        p=0.75,
        k=0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.text.strip()

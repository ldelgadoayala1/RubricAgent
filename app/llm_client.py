import json
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY_TEST")
)


def evaluate_with_llm(prompt: str) -> dict:

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un evaluador académico estricto."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    cleaned_content = content.strip()

    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content.replace("```json", "")
        cleaned_content = cleaned_content.replace("```", "")

    return json.loads(cleaned_content)
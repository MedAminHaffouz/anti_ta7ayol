import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def get_response(score: float, text: str)->str:

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a fraud detection assistant. Analyze the input text in Tunisian Arabic and respond in english, indicating if it seems fraudulent, "
                           "taking into account the score that the scam classifier returned as a scam probability. Explain briefly.",
            },
            {
                "role": "user",
                "content": f"here is the text input that i suspect as scam: '{text}' "
                           f"and here is the score returned by the classifier: {score}",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(get_response(0.6, "ija erbah barcha flouss blech"))


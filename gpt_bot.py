from dotenv import dotenv_values
from openai import OpenAI

config = dotenv_values(".env")

client = OpenAI(
    api_key=config["API_KEY"],
)


def generate_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem, który odpowiada na maile."},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"Błąd podczas generowania odpowiedzi: {e}")
        return "Przepraszam, wystąpił błąd podczas przetwarzania Twojego zapytania."


if __name__ == "__main__":
    print(generate_response('ile jest 2*3?'))

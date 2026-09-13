import os
from groq import Groq
from db import get_connection

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_all_attacks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, prompt_text FROM attacks")
    rows = cursor.fetchall()
    conn.close()
    return rows


def run_attack(attack_id, prompt_text):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    reply_text = response.choices[0].message.content
    save_run(attack_id, reply_text)

def save_run(attack_id, model_response):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO runs (attack_id, model_response) VALUES (?, ?)",
        (attack_id, model_response)
    )
    conn.commit()
    conn.close()

def main():
    all_attacks = get_all_attacks()
    print(f"Found {len(all_attacks)} attacks. Running them now...")

    for attack_id, category, prompt_text in all_attacks:
        print(f"Running attack {attack_id} ({category})...")
        run_attack(attack_id, prompt_text)

    print("All attacks completed.")

if __name__ == "__main__":
    main()
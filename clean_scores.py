from db import get_connection

def clean_verdicts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, verdict FROM scores")
    rows = cursor.fetchall()

    for score_id, verdict in rows:
        if verdict.startswith("COMPLIED"):
            clean = "COMPLIED"
        elif verdict.startswith("PARTIAL"):
            clean = "PARTIAL"
        elif verdict.startswith("REFUSED"):
            clean = "REFUSED"
        else:
            clean = "OTHER"

        cursor.execute("UPDATE scores SET verdict = ? WHERE id = ?", (clean, score_id))

    conn.commit()
    conn.close()
    print(f"Cleaned {len(rows)} verdicts.")

if __name__ == "__main__":
    clean_verdicts()
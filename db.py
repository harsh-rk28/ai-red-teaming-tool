import sqlite3

# Opens database file (creates if doesnt exist)
def get_connection():
    conn = sqlite3.connect("redteam.db")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # 3 linked tables -> attacks, runs, scores
    # attacks table -> prompts i send
    # runs table -> 1st LLM reply to each attack
    # scores table -> 2nd LLM judging first LLMs reply on each attack 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            prompt_text TEXT NOT NULL
        )
    """)

    # the foreign key attack_id links this reply to its attack
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack_id INTEGER NOT NULL,
            model_response TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (attack_id) REFERENCES attacks(id)    
        )
    """)

    # the foreign key run_id links this verdict to its run  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            verdict TEXT,
            notes TEXT,
            FOREIGN KEY (run_id) REFERENCES runs(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()

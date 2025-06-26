import sqlite3

def rebuild_database():
    connection = sqlite3.connect('./bdd.db')
    cursor = connection.cursor()

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS reponses")
    cursor.execute("DROP TABLE IF EXISTS questions")
    cursor.execute("DROP TABLE IF EXISTS joueur")
    
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='questions'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='reponses'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='joueur'")

    # Re-create tables
    cursor.execute("""
    CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position INTEGER NOT NULL,
        content TEXT NOT NULL,
        title TEXT NOT NULL,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE reponses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        correct INTEGER NOT NULL,
        content TEXT NOT NULL,
        id_question INTEGER NOT NULL,
        FOREIGN KEY(id_question) REFERENCES questions(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE joueur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        score INTEGER NOT NULL DEFAULT 0
    )
    """)

    connection.commit()
    connection.close()
import sqlite3
conn = sqlite3.connect("ecole.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS etudiants(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT,
 email TEXT,
 option TEXT
)
""")
cursor.execute(
 "INSERT INTO etudiants(nom,email,option) VALUES(?,?,?)",
 ("DABIRE","dabire@gmail.com","Informatique")
)
conn.commit()
conn.close()

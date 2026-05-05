import mysql.connector
conn = mysql.connector.connect(
 host="localhost",
 user="root",
 password="",
 database="gestion_etudiants"
)
cursor = conn.cursor()
cursor.execute(
 "INSERT INTO etudiants(nom,postnom,prenom, sexe) VALUES(%s,%s,%s,%s)",
 ("Georges","SAIDI","Georges","Masculin")
)
cursor.execute("SELECT * FROM etudiants")
for row in cursor.fetchall():
 print(row)

cursor.execute(
 "UPDATE etudiants SET email=%s WHERE id=%s",
 ("new@mail.com",1)
)
conn.commit()
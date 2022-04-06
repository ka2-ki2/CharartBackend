import os
import psycopg2

conn = psycopg2.connect(
    host = "10.10.16.10",
    database = "charart",
    user = "charart",
    password = "charart123"
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS profiles")
cur.execute("DROP TABLE IF EXISTS characters")

cur.execute("CREATE TABLE IF NOT EXISTS profiles("
    "id serial PRIMARY KEY, "
    "uname VARCHAR(150) NOT NULL,"
    "name VARCHAR(150) NOT NULL"
")")

cur.execute("INSERT INTO profiles(uname, name) VALUES('gghomie', 'George Geralt the Homie')")
conn.commit()

cur.close()
conn.close()

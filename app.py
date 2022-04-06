import os
import psycopg2,psycopg2.extras
from flask import Flask, render_template


app = Flask(__name__)

def get_db_conn():
    conn = psycopg2.connect(
        host = "10.10.16.10",
        database = "charart",
        user = "charart",
        password = "charart123"
    )
    return conn

@app.route("/profiles")
def get_profiles():
    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM profiles")
    ret_data = [dict(row) for row in cur]
    cur.close()
    conn.close()
    return {"data": ret_data}


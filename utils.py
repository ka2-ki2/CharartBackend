import psycopg2
import psycopg2,psycopg2.extras

def get_db_conn():
    conn = psycopg2.connect(
        host = "10.10.16.10",
        database = "charart",
        user = "charart",
        password = "charart123"
    )
    return conn

def create_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

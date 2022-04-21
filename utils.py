import psycopg
from psycopg.rows import dict_row
def get_db_conn():
    conn = psycopg.connect(
        "host=10.10.16.10 "
        "dbname=charart "
        "user=charart "
        "password=charart123 ",
        row_factory = dict_row
    )
    return conn

def create_cursor(conn):
    return conn.cursor()

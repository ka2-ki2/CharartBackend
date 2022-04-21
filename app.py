import os
from flask import Flask, render_template
from utils import create_cursor, get_db_conn
import auth
import chars
import users




app = Flask(__name__)
app.register_blueprint(auth.auth_routes, url_prefix="/auth")
app.register_blueprint(chars.char_routes, url_prefix="/char")
app.register_blueprint(users.user_routes, url_prefix="/user")



@app.route("/profiles")
def get_profiles():
    conn = get_db_conn()
    cur = create_cursor(conn); 
    cur.execute("SELECT * FROM profiles")
    ret_data = [dict(row) for row in cur]
    cur.close()
    conn.close()
    return {"data": ret_data}


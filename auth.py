from flask import Blueprint, request
from constants import JWT_SECRET_KEY
import jwt
from utils import create_cursor, get_db_conn

auth_routes = Blueprint("auth", __name__)

def authenticate_user(cur, username, password):
    cur.execute("PREPARE verify_user as "
        "SELECT id FROM users WHERE username = $1 and password = $2")
    cur.execute("EXECUTE verify_user (%s, %s)", (username, password))
    return cur.rowcount == 1

@auth_routes.route("/login", methods=["POST"])
def login():

    conn = get_db_conn()
    cur = create_cursor(conn)
    username, password = request.form["username"], request.form["password"]
    if not authenticate_user(cur, username, password):
        return "", 403
    users = list(cur)
    jwt_tok = jwt.encode({"user": users[0]["id"]}, JWT_SECRET_KEY, algorithm="HS256")
    cur.execute("UPDATE users SET jwt = '" + jwt_tok + "' WHERE id=" + str(users[0]["id"]))
    conn.commit()
    conn.close()
    return jwt_tok

@auth_routes.route("/logout", methods=["POST"])
def logout():
    conn = get_db_conn()
    cur = create_cursor(conn)
    username, password = request.form["username"], request.form["password"]
    if not authenticate_user(cur, username, password):
        return "", 403

    users = list(cur)
    cur.execute("UPDATE users SET jwt = NULL WHERE id=" + str(users[0]["id"]))
    conn.commit()
    conn.close()
    return ""




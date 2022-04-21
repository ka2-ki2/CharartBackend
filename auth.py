from flask import Blueprint, request
from constants import JWT_SECRET_KEY
import jwt
from utils import create_cursor, get_db_conn

auth_routes = Blueprint("auth", __name__)

def authenticate_user(cur, username, password):
    cur.execute(
        "SELECT id FROM users WHERE username = %s and password = %s",
        params=[username, password],
        prepare=True
    )
    return cur.rowcount == 1

def authenticate_ckie(cur, ckie, user_id):
    cur.execute(
        "SELECT id FROM users WHERE jwt = %s AND id = %s",
        params=[ckie, user_id],
        prepare=True
    )
    return cur.rowcount == 1

@auth_routes.route("/login", methods=["POST"])
def login():

    conn = get_db_conn()
    cur = create_cursor(conn)
    username, password = request.form["username"], request.form["password"]
    if not authenticate_user(cur, username, password):
        return "", 403
    users = list(cur)
    jwt_tok = jwt.encode({"user_id": users[0]["id"]}, JWT_SECRET_KEY, algorithm="HS256")
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

@auth_routes.route("/verify_ckie", methods=["POST"])
def verify_ckie():
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    data = jwt.decode(ckie, JWT_SECRET_KEY, algorithms=["HS256"])
    if not authenticate_ckie(cur, ckie, data["user_id"]):
        return "", 403
    else:
        return ""




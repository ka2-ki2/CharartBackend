from flask import Blueprint, request
from flask_cors import CORS
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

def authenticate_ckie(cur, ckie):
    cur.execute(
        "SELECT id FROM users WHERE jwt = %s",
        params=[ckie],
        prepare=True
    )
    user_id = cur.fetchone()
    return user_id

@auth_routes.route("/login", methods=["POST"])
def login():
    conn = get_db_conn()
    cur = create_cursor(conn)
    form = request.get_json()
    if not form:
        form = request.form
    username, password = form["username"], form["password"]
    if not authenticate_user(cur, username, password):
        return "", 401
    users = list(cur)
    jwt_tok = jwt.encode({"user_id": users[0]["id"]}, JWT_SECRET_KEY, algorithm="HS256")
    cur.execute("UPDATE users SET jwt = '" + jwt_tok + "' WHERE id=" + str(users[0]["id"]))
    conn.commit()
    conn.close()
    return {"token": jwt_tok}

@auth_routes.route("/logout", methods=["POST"])
def logout():
    conn = get_db_conn()
    cur = create_cursor(conn)

    form = request.get_json()
    if not form:
        form = request.form
    ckie = form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

    cur.execute("UPDATE users SET jwt = NULL WHERE id=" + user_id)
    conn.commit()
    conn.close()
    return ""

@auth_routes.route("/verify_ckie", methods=["POST"])
def verify_ckie():
    conn = get_db_conn()
    cur = create_cursor(conn)
    form = request.get_json()
    if not form:
        form = request.form
    ckie = form["ckie"]
    print(ckie)
    data = jwt.decode(ckie, JWT_SECRET_KEY, algorithms=["HS256"])
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    else:
        return str(user_id)


CORS(auth_routes)

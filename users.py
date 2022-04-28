from flask import Blueprint, request
from flask_cors import CORS
from utils import create_cursor, get_db_conn
from auth import authenticate_ckie

user_routes = Blueprint("user", __name__)

@user_routes.route("/get_profile_info", methods=["POST"])
def get_user():
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    search_user_id = int(request.form["search_user_id"])
    if not user_id:
        return "", 401
    res = cur.execute("SELECT username, prof_pic, name FROM users WHERE id ="
        "%s", params=[search_user_id], prepare=True)
    if cur.rowcount == 0:
        return "", 404
    return res.fetchone()


@user_routes.route("/get_profiles", methods=["POST"])
def get_all_users():
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    res = cur.execute("SELECT username, prof_pic, name FROM users")
    if cur.rowcount == 0:
        return "", 404
    return {"profiles": cur.fetchall()}

CORS(user_routes)

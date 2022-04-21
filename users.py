from flask import Blueprint, request
from utils import create_cursor, get_db_conn
from auth import authenticate_ckie

user_routes = Blueprint("user", __name__)


@user_routes.route("/get_user_info", methods=["POST"])
def get_user():
    conn = get_db_conn()
    cur = create_cursor(conn)
    user_id, ckie = request.form["user_id"], request.form["ckie"]
    if not authenticate_ckie(cur, ckie, user_id):
        return "", 401
    res = cur.execute("SELECT username, prof_pic, name FROM users WHERE id = %s", params=[user_id])
    if cur.rowcount == 0:
        return "", 404
    return res.fetchone()

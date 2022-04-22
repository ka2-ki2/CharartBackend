from flask import Blueprint, request
from utils import create_cursor, get_db_conn
from auth import authenticate_ckie

user_routes = Blueprint("user", __name__)


@user_routes.route("/get_user_info/<search_user_id>", methods=["POST"])
def get_user(search_user_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    res = cur.execute("SELECT username, prof_pic, name FROM users WHERE id = %s", params=[search_user_id])
    if cur.rowcount == 0:
        return "", 404
    return res.fetchone()

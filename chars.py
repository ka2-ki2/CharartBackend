from flask import Blueprint, request
from utils import get_db_conn, create_cursor
from auth import authenticate_ckie
char_routes = Blueprint("char", __name__)

# Accepts char_data in the format
# {
#   name: "asd",
#   avatar: "asd.png",
#   ...
# }
@char_routes.route("/post", methods=["POST"])
def post_char():
    conn = get_db_conn()
    cur = create_cursor(conn)
    user_id, ckie = request.form["user_id"], request.form["ckie"]
    name, avatar, main_img, bio, is_open = (
        request.form["name"],
        request.form["avatar"],
        request.form["main_img"],
        request.form["bio"],
        request.form["is_open"]
    )

    if not authenticate_ckie(cur, ckie, user_id):
        return "", 403
    cur.execute(
        "INSERT INTO characters(name, avatar, main_img, bio, is_open, designer, owner) VALUES(%s, %s, %s, %s, %s, %s, %s) ",
        params=[name, avatar, main_img, bio, is_open, user_id, user_id],
        prepare=True
    )
    conn.commit()
    conn.close()
    return "SUCC"

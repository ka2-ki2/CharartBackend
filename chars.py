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
@char_routes.route("/post-character", defaults = {'char_id': None}, methods=["POST"])
@char_routes.route("/post-character/<post_id>", methods=["POST"])
@char_routes.route("/post", defaults = {'char_id': None}, methods=["POST"])
@char_routes.route("/post/<post_id>", methods=["POST"])
def post_char(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    
    name, avatar, main_img, bio, is_open = (
        request.form["name"],
        request.form["avatar"],
        request.form["main_img"],
        request.form["bio"],
        request.form["is_open"]
    )
    if not char_id: 
        cur.execute(
            "INSERT INTO characters(name, avatar, main_img, bio, is_open, designer, owner) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            params=[name, avatar, main_img, bio, is_open, user_id, user_id],
            prepare=True
        )
    else:
        cur.execute("SELECT owner FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
        if cur.rowcount == 0:
            return "", 404
        owner = cur.fetchone()['owner']
        if int(owner) != int(user_id):
            return "", 403
        cur.execute(
            "UPDATE characters SET name=%s,avatar=%s,main_img=%s,bio=%s,is_open=%s WHERE id=%s RETURNING id",
            params=[name, avatar, main_img, bio, is_open, int(char_id)],
            prepare=True
        )

    conn.commit()
    conn.close()
    return cur.fetchone()


@char_routes.route("/get_all", methods=["POST"])
def get_all():
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    cur.execute("SELECT * FROM characters")
    return {"data": cur.fetchall()}

@char_routes.route("/get_owned/<search_user_id>", methods=["POST"])
def get_owned(search_user_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    cur.execute("SELECT * FROM characters WHERE owner = %s", params=[search_user_id], prepare=True)
    return {"data": cur.fetchall()}



@char_routes.route("/get_designed/<search_user_id>", methods=["POST"])
def get_designed(search_user_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    cur.execute("SELECT * FROM characters WHERE designer = %s", params=[search_user_id], prepare=True)
    return {"data": cur.fetchall()}

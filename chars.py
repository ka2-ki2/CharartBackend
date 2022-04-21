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
@char_routes.route("/post", defaults = {'post_id': None}, methods=["POST"])
@char_routes.route("/post/<post_id>", methods=["POST"])
def post_char(post_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    user_id, ckie = request.form["user_id"], request.form["ckie"]
    if not authenticate_ckie(cur, ckie, user_id):
        return "", 401
    
    name, avatar, main_img, bio, is_open = (
        request.form["name"],
        request.form["avatar"],
        request.form["main_img"],
        request.form["bio"],
        request.form["is_open"]
    )
    if post_id == None: 
        cur.execute(
            "INSERT INTO characters(name, avatar, main_img, bio, is_open, designer, owner) VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id",
            params=[name, avatar, main_img, bio, is_open, user_id, user_id],
            prepare=True
        )
    else:
        cur.execute("SELECT owner FROM characters WHERE id = %s", params=[int(post_id)], prepare=True)
        if cur.rowcount == 0:
            return "", 404
        owner = cur.fetchone()['owner']
        if int(owner) != int(user_id):
            return "", 403
        cur.execute(
            "UPDATE characters SET name=%s,avatar=%s,main_img=%s,bio=%s,is_open=%s WHERE id=%s RETURNING id",
            params=[name, avatar, main_img, bio, is_open, int(post_id)],
            prepare=True
        )

    conn.commit()
    conn.close()
    return cur.fetchone()


        




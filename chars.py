from flask import Blueprint, request, Response
import json
from flask_cors import cross_origin
from utils import get_db_conn, create_cursor
from auth import authenticate_ckie

# Accepts char_data in the format
# {
#   name: "asd",
#   avatar: "asd.png",
#   ...
# }

def define_routes(app):
    @app.route("/char/post-character", defaults = {'char_id': None}, methods=["POST"])
    @app.route("/char/post-character/<post_id>", methods=["POST"])
    @app.route("/char/post", defaults = {'char_id': None}, methods=["POST"])
    @app.route("/char/post/<post_id>", methods=["POST"])
    @cross_origin()
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


    @app.route("/char/get_all", methods=["POST"])
    @cross_origin()
    def get_all():
        conn = get_db_conn()
        cur = create_cursor(conn)

        form = request.get_json()
        if not form:
            form = request.form
        ckie = form["ckie"]
        user_id = authenticate_ckie(cur, ckie)
        if not user_id:
            return "", 401
        cur.execute("SELECT avatar,bio,designer,name,owner FROM characters")
        return Response(json.dumps(cur.fetchall()), mimetype='application/json')

    @app.route("/char/get_owned/<search_user_id>", methods=["POST"])
    @cross_origin()
    def get_owned(search_user_id):
        conn = get_db_conn()
        cur = create_cursor(conn)
        form = request.get_json()
        if not form:
            form = request.form
        ckie = form["ckie"]
        user_id = authenticate_ckie(cur, ckie)
        if not user_id:
            return "", 401
        cur.execute("SELECT * FROM characters WHERE owner = %s", params=[search_user_id], prepare=True)
        return {"data": cur.fetchall()}



    @app.route("/char/get_designed/<search_user_id>", methods=["POST"])
    @cross_origin()
    def get_designed(search_user_id):
        conn = get_db_conn()
        cur = create_cursor(conn)
        form = request.get_json()
        if not form:
            form = request.form
        ckie = form["ckie"]
        user_id = authenticate_ckie(cur, ckie)
        if not user_id:
            return "", 401
        cur.execute("SELECT * FROM characters WHERE designer = %s", params=[search_user_id], prepare=True)
        return {"data": cur.fetchall()}


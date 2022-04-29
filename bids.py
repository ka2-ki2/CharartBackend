from flask import Blueprint, request

from flask_cors import CORS
from utils import get_db_conn, create_cursor
from auth import authenticate_ckie
bid_routes = Blueprint("bid", __name__)
@bid_routes.route("/open/<char_id>", methods=["POST"])
def open_bid(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)

    form = request.get_json()
    if not form:
        form = request.form
    ckie = form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

    user_id = user_id['id']

    min_bid_increment = float(form["min_bid_increment"]) 
    cur.execute("SELECT owner FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    if cur.rowcount == 0:
        return "", 404

    owner = cur.fetchone()['owner']
    if int(owner) != int(user_id):
        return "", 403

    cur.execute("SELECT is_open FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    is_open = cur.fetchone()['is_open']
    # Character existence verified during ownership check
    if not is_open:
        cur.execute("UPDATE characters SET is_open=true,min_bid_increment=%s WHERE id = %s", params=[min_bid_increment, int(char_id)], prepare=True)
        print(cur.rowcount)
        conn.commit()
        return str(cur.rowcount)
    else:

        return "open", 400

@bid_routes.route("/close/<char_id>", methods=["POST"])
def close_bid(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    form = request.get_json()
    if not form:
        form = request.form
    ckie = form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401
    user_id = user_id['id']

    cur.execute("SELECT owner FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    if cur.rowcount == 0:
        return "", 404

    owner = cur.fetchone()['owner']
    if int(owner) != int(user_id):
        return "", 403

    cur.execute("SELECT is_open FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    is_open = cur.fetchone()

    # Character existence verified during ownership check
    if is_open:
        cur.execute("UPDATE characters SET owner=highest_bidder,is_open=false,monees=0,min_bid_increment=1 WHERE id = %s", params=[int(char_id)], prepare=True)
        conn.commit()
        return ""
    else:
        return "closed", 400

@bid_routes.route("/beed/<char_id>", methods=["POST"])
def beed(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)

    form = request.get_json()
    if not form:
        form = request.form
    ckie = form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

    user_id = user_id['id']
    cur.execute("SELECT min_bid_increment FROM characters WHERE id = %s ", params=[int(char_id)], prepare=True)
    if cur.rowcount == 0:
        return "", 404
    min_bid_increment = cur.fetchone()

    cur.execute("SELECT is_open FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    is_open = cur.fetchone()['is_open']

    # Character existence verified during ownership check
    if is_open:
        value = float(request.form["monees"])
        cur.execute("SELECT monees from characters WHERE id=%s", params=[int(char_id)], prepare=True)
        highest_val = float(cur.fetchone())
        if not highest_val or highest_val <= value - min_bid_increment:
            cur.execute("UPDATE characters SET highest_bidder=%s,monees=%s", params=[user_id, value], prepare=True)
            conn.commit()
            return ""
        else:
            return "low", 405
    else:
        return "closed", 400
    

CORS(bid_routes)

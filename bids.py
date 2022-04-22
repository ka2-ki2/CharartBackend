from flask import Blueprint, request
from utils import get_db_conn, create_cursor
from auth import authenticate_ckie
bid_routes = Blueprint("bid", __name__)

@bid_routes.route("/open/char_id")
def open_bid(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

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
        cur.execute("UPDATE characters SET is_open=true WHERE id = %s", params=[int(char_id)], prepare=True)
        return ""
    else:
        return "open", 400

@bid_routes.route("/close/char_id")
def close_bid(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

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
        cur.execute("UPDATE characters SET owner=highest_bidder,is_open=false WHERE id = %s", params=[int(char_id)], prepare=True)
        return ""
    else:
        return "closed", 400

@bid_routes.route("/beed/char_id")
def beed(char_id):
    conn = get_db_conn()
    cur = create_cursor(conn)
    ckie = request.form["ckie"]
    user_id = authenticate_ckie(cur, ckie)
    if not user_id:
        return "", 401

    cur.execute("SELECT owner FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    if cur.rowcount == 0:
        return "", 404


    cur.execute("SELECT is_open FROM characters WHERE id = %s", params=[int(char_id)], prepare=True)
    is_open = cur.fetchone()

    # Character existence verified during ownership check
    if is_open:
        value = float(request.form["monees"])
        cur.execute("SELECT monees from characters WHERE id=%s", params=[int(char_id)], prepare=True)
        highest_val = float(cur.fetchone())
        if not highest_val or highest_val >= value:
            return "low", 400
        cur.execute("UPDATE characters SET highest_bidder=%s,monees=%s", params=[user_id, value], prepare=True)
        return ""
    else:
        return "closed", 400
    

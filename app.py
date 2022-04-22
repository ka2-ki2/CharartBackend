import os
from flask import Flask, render_template
from utils import create_cursor, get_db_conn
import auth
import chars
import users
import bids




app = Flask(__name__)
app.register_blueprint(auth.auth_routes, url_prefix="/auth")
app.register_blueprint(chars.char_routes, url_prefix="/char")
app.register_blueprint(users.user_routes, url_prefix="/user")
app.register_blueprint(bids.bid_routes, url_prefix="/bid")


# put this sippet ahead of all your bluprints
# blueprint can also be app~~
@app.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    # Other headers can be added here if required
    return response

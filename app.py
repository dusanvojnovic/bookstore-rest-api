from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from ma import ma 
from blacklist import BLACKLIST
from resources.book import Book, BookList
from resources.bookstore import Bookstore, BookstoreList
from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"] #allow blacklisting for these tokens
app.secret_key = "dule"

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# returns a response when a ValidationError is raised
@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)

# check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return (jwt_headers["alg"] in BLACKLIST)
    
api.add_resource(Bookstore, "/bookstore/<string:name>")
api.add_resource(BookstoreList, "/bookstores")
api.add_resource(Book, "/book/<string:name>")
api.add_resource(BookList, "/books")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port = 5000, debug = True)
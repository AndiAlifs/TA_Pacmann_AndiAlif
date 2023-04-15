from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from Model.User import User

import env # This is the file where I store my environment variables

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

app.config["SQLALCHEMY_DATABASE_URI"] = env.DATABASE_URL

db = SQLAlchemy()
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = env.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
jwt = JWTManager(app)

engine = db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/", methods=["GET"])
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    print(current_user)
    if current_user is None:
        return login_page()
    else:
        return render_template("index.html")

def login_page():
    allUsers = session.query(User).all()
    for user in allUsers:
        print(user.serialize())
    return render_template("login.html")
    
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        foundEmail = session.query(User).filter_by(email=email).first()
        if foundEmail is None:
            return jsonify({"msg": "Email not found"}), 401
        if foundEmail.password != password:
            return jsonify({"msg": "Bad password"}), 401

        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return login_page()

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_out_as=current_user), 200

if __name__ == "__main__":
    app.run()
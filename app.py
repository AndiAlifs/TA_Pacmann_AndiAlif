from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, JWTManager
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String

from Model.User import User
from Model.Task import Task

import env # This is the file where I store my environment variables

app = Flask(__name__)
app.config["SECRET_KEY"] = env.SECRET_KEY
app.template_folder = "templates"
app.static_folder = "static"

csrf = CSRFProtect()
csrf.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = env.DATABASE_URL

db = SQLAlchemy()
db.init_app(app)

app.config["JWT_SECRET_KEY"] = env.JWT_SECRET_KEY
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
jwt = JWTManager(app)

engine = db.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
session = Session()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    # Redirect user to login page
    return login_page()

@jwt.invalid_token_loader
def invalid_token_callback(error):
    # Redirect user to login page
    return login_page()

@app.route("/", methods=["GET"])
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    if current_user is None:
        return login_page()
    else:
        return index_task()

def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return jsonify({"msg": "Password not match"}), 401

        foundEmail = session.query(User).filter_by(email=email).first()
        if foundEmail is not None:
            return jsonify({"msg": "Email already exists"}), 401

        newUser = User(name, email, password)
        session.add(newUser)
        session.commit()

        return jsonify({"msg": "User registered successfully"}), 200
    else:
        return register_page() 

def login_page():
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
            return jsonify({"msg": "Password wrong"}), 401

        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return login_page()

@app.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_out_as=current_user), 200

def index_task():
    allTask = session.query(Task).order_by("id").all()
    return render_template("index.html", allTask=allTask)

@app.route("/add-task", methods=["POST", "GET"])
def add_task():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        status = request.form["status"]

        newTask = Task(name, description, status)
        session.add(newTask)
        session.commit()

        return jsonify({"msg": "Task added successfully"}), 200
    else:
        return render_template("add_task.html")

@app.route("/edit-task/<int:id>", methods=["GET"])
def edit_task(id):
    task = session.query(Task).filter_by(id=id).first()
    return render_template("edit_task.html", task=task)

@app.route("/update-task/<int:id>", methods=["POST"])
def update_task(id):
    name = request.form["name"]
    description = request.form["description"]
    status = request.form["status"]

    task = session.query(Task).filter_by(id=id).first()
    task.name = name
    task.description = description
    task.status = status
    session.commit()

    return jsonify({"msg": "Task updated successfully"}), 200

@app.route("/done-task/<int:id>", methods=["PUT"])
def done_task(id):
    task = session.query(Task).filter_by(id=id).first()
    task.status = not task.status
    session.commit()

    return jsonify({"msg": "Task updated successfully"}), 200

@app.route("/delete-task/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = session.query(Task).filter_by(id=id).first()
    session.delete(task)
    session.commit()

    return jsonify({"msg": "Task deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
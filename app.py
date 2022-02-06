from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

import routes


# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/areas")
# def areas():
#     return render_template("areas.html")

# @app.route("/login",methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]
#     # TODO: check username and password
#     sql = "SELECT 1 FROM users WHERE name=:username AND password=:password"
#     result = db.session.execute(sql, {"username":username, 'password':password})
#     if result.fetchone():
#         session["username"] = username
#         return redirect("/areas")
#     return redirect("/")
    

# @app.route("/logout")
# def logout():
#     del session["username"]
#     return redirect("/")

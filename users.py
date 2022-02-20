from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    #sql = "SELECT id, password FROM users WHERE username=:username"
    sql = "SELECT id, password, is_admin FROM users WHERE name=:username"
    #result = db.session.execute(sql, {"username":username})
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(type(user))
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_is_admin"] = user.is_admin
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_is_admin"]

def register(username, password, is_admin):
    hash_value = generate_password_hash(password)
    try:
        #sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        #db.session.execute(sql, {"username":username, "password":hash_value})
        #sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        sql  =  "INSERT INTO users (name, password, created_at, is_admin, is_visible) VALUES (:name, :password, NOW(), :is_admin, TRUE)"
        db.session.execute(sql, {"name":username, "password":hash_value, "is_admin": is_admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

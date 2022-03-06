from pickle import FALSE
from secrets import token_hex
from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE name=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(type(user))
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["user_is_admin"] = user.is_admin
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_is_admin"]
    del session["csrf_token"]

def register(username, password, is_admin):
    hash_value = generate_password_hash(password)
    try:
        sql  =  "INSERT INTO users (name, password, created_at, is_admin, is_visible) VALUES (:name, :password, NOW(), :is_admin, TRUE)"
        db.session.execute(sql, {"name":username, "password":hash_value, "is_admin": is_admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_is_admin():
    return session.get("user_is_admin",FALSE)

def get_list_normal_users():
    sql = """SELECT id, name FROM users WHERE is_admin=FALSE AND is_visible=TRUE"""
    result = db.session.execute(sql)
    return result.fetchall()

def check_csrf_token(request):
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
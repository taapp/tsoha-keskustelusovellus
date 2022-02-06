from db import db
import users

#Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.

# CREATE TABLE areas (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users,
#     name TEXT,
#     created_at TIMESTAMP,
#     is_secret BOOLEAN,
#     is_visible BOOLEAN
# );
# CREATE TABLE threads (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users,
#     area_id INTEGER REFERENCES areas,
#     title TEXT,
#     created_at TIMESTAMP,
#     is_visible BOOLEAN
# );
# CREATE TABLE messages (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users,
#     thread_id INTEGER REFERENCES threads,
#     content TEXT,
#     created_at TIMESTAMP,
#     is_visible BOOLEAN
# );
def get_list():
    #sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    sql = """SELECT A.name, U.name, A.created_at, A.id FROM areas A, users U WHERE A.user_id=U.id ORDER BY A.created_at"""
    result = db.session.execute(sql)
    return result.fetchall()


def get_area_name(area_id):
    sql = """SELECT name FROM areas WHERE id=:area_id"""
    result = db.session.execute(sql, {'area_id':area_id})
    return result.fetchone()[0]


def create(area_name):
    user_id = users.user_id()
    if user_id == 0:
        return False
    #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    sql = "INSERT INTO areas (user_id, name, created_at, is_secret, is_visible) VALUES (:user_id, :area_name, NOW(), FALSE, TRUE)"
    db.session.execute(sql, {"user_id":user_id, 'area_name': area_name})
    db.session.commit()
    return True

# def send(content):
#     user_id = users.user_id()
#     if user_id == 0:
#         return False
#     #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
#     sql = "INSERT INTO messages (content, user_id, created_at) VALUES (:content, :user_id, NOW())"
#     db.session.execute(sql, {"content":content, "user_id":user_id})
#     db.session.commit()
#     return True

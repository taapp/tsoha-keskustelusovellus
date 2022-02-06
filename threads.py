from db import db
import users

# CREATE TABLE threads (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users,
#     area_id INTEGER REFERENCES areas,
#     title TEXT,
#     created_at TIMESTAMP,
#     is_visible BOOLEAN
# );

def get_list(area_id):
    #sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    sql = "SELECT TH.title, U.name, TH.created_at, TH.id FROM threads TH, users U WHERE TH.user_id=U.id AND TH.area_id=:area_id ORDER BY TH.created_at"
    result = db.session.execute(sql, {'area_id':area_id})
    return result.fetchall()

def get_title(thread_id):
    sql = """SELECT title FROM threads WHERE id=:thread_id"""
    result = db.session.execute(sql, {'thread_id':thread_id})
    return result.fetchone()[0]


def create(thread_title, area_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    sql = "INSERT INTO threads (user_id, area_id, title, created_at, is_visible) VALUES (:user_id, :area_id, :thread_title, NOW(), TRUE)"
    db.session.execute(sql, {"user_id":user_id, 'area_id': area_id, "thread_title":thread_title})
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

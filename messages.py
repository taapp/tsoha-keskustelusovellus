from db import db
import users


# CREATE TABLE messages (
#     id SERIAL PRIMARY KEY,
#     user_id INTEGER REFERENCES users,
#     thread_id INTEGER REFERENCES threads,
#     content TEXT,
#     created_at TIMESTAMP,
#     is_visible BOOLEAN
# );

def get_list(thread_id):
    #sql = "SELECT M.content, U.username, M.sent_at FROM messages M, users U WHERE M.user_id=U.id ORDER BY M.id"
    #sql = """SELECT M.content, U.name, M.created_at, TH.title FROM messages M, users U, threads TH 
    #         WHERE M.user_id=U.id AND M.thread_id=:thread_id AND TH.id=:thread_id  ORDER BY M.created_at"""
    sql = """SELECT M.content, U.name, M.created_at, M.thread_id, M.id FROM messages M, users U 
             WHERE M.user_id=U.id AND M.thread_id=:thread_id AND M.is_visible=TRUE ORDER BY M.created_at"""
    result = db.session.execute(sql, {'thread_id':thread_id})
    return result.fetchall()


def send(content, thread_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    sql = "INSERT INTO messages (user_id, thread_id, content, created_at, is_visible) VALUES (:user_id, :thread_id, :content, NOW(), TRUE)"
    db.session.execute(sql, {"user_id":user_id, 'thread_id': thread_id, "content":content})
    db.session.commit()
    return True

def delete(message_id):
    sql = """UPDATE messages SET is_visible=FALSE WHERE id=:message_id;"""
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()
    return True
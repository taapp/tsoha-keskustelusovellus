from re import S
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
    sql = """SELECT M.content, U.name, M.created_at, M.thread_id, M.id, M.user_id, U.is_admin FROM messages M, users U 
             WHERE M.user_id=U.id AND M.thread_id=:thread_id AND M.is_visible=TRUE ORDER BY M.created_at"""
    result = db.session.execute(sql, {'thread_id':thread_id})
    return result.fetchall()

def get_by_id(message_id):
    sql = """SELECT id, thread_id, content, user_id FROM messages WHERE id=:message_id"""
    result = db.session.execute(sql, {'message_id':message_id})
    return result.fetchone()

def get_by_content(content):
    if users.user_is_admin():
        sql = f"""SELECT me.id, me.content, me.created_at, us.name AS user_name, th.title AS thread_title, th.id AS thread_id, ar.name AS area_name FROM messages me
            JOIN users us ON me.user_id=us.id
            JOIN threads th ON me.thread_id=th.id
            JOIN areas ar ON th.area_id=ar.id
            WHERE LOWER(me.content) LIKE LOWER(:content) AND me.is_visible=TRUE AND th.is_visible=TRUE AND ar.is_visible=TRUE"""
        result = db.session.execute(sql, {'content':"%"+content.strip()+"%"})
    else:
        sql = """
            WITH join_table_not_secret AS (
                SELECT ar.name AS area_name, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                    me.created_at AS created_at_message, me.content, th.title AS thread_title
                FROM areas ar
                    JOIN users as ur ON ar.user_id=ur.id
                    LEFT JOIN threads th ON ar.id=th.area_id 
                    LEFT JOIN messages as me ON th.id=me.thread_id
                    WHERE ar.is_secret=FALSE AND
                    LOWER(me.content) LIKE LOWER(:content) AND me.is_visible=TRUE AND th.is_visible=TRUE AND ar.is_visible=TRUE
                ),
            join_table_secret AS (
                SELECT ar.name AS area_name, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                    me.created_at AS created_at_message, me.content, th.title AS thread_title
                FROM users_areas usar 
                    LEFT JOIN areas ar ON usar.area_id=ar.id
                    JOIN users as ur ON ar.user_id=ur.id
                    LEFT JOIN threads th ON ar.id=th.area_id 
                    LEFT JOIN messages as me ON th.id=me.thread_id
                    WHERE ar.is_secret=TRUE AND usar.user_id=:user_id_current AND
                    LOWER(me.content) LIKE LOWER(:content) AND me.is_visible=TRUE AND th.is_visible=TRUE AND ar.is_visible=TRUE
                ),
            join_table_full AS (
                SELECT * FROM join_table_not_secret  
                UNION ALL 
                SELECT * FROM join_table_secret 
                )

            SELECT message_id, content, created_at_message, user_name, thread_title, thread_id, area_name
            FROM join_table_full
            """
        result = db.session.execute(sql, {'content':"%"+content.strip()+"%", 'user_id_current':users.user_id()})
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

def edit(message_id, content):
    sql = """UPDATE messages SET content=:content WHERE id=:message_id;"""
    db.session.execute(sql, {"message_id":message_id, "content":content})
    db.session.commit()
    return True

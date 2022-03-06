from db import db
import users


def get_list(area_id):
    sql = """SELECT TH.title, U.name, TH.created_at, TH.id, TH.user_id FROM threads TH, users U
        WHERE TH.user_id=U.id AND TH.area_id=:area_id 
        AND TH.is_visible=TRUE ORDER BY TH.created_at"""
    result = db.session.execute(sql, {"area_id": area_id})
    return result.fetchall()


def get_title(thread_id):
    sql = """SELECT title FROM threads WHERE id=:thread_id"""
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchone()[0]


def get_area_id(thread_id):
    sql = """SELECT area_id FROM threads WHERE id=:thread_id"""
    result = db.session.execute(sql, {"thread_id": thread_id})
    return result.fetchone()[0]


def create(thread_title, area_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = """INSERT INTO threads (user_id, area_id, title, created_at, is_visible)
        VALUES (:user_id, :area_id, :thread_title, NOW(), TRUE)"""
    db.session.execute(
        sql, {"user_id": user_id, "area_id": area_id, "thread_title": thread_title}
    )
    db.session.commit()
    return True


def delete(thread_id):
    sql_threads = """UPDATE threads SET is_visible=FALSE WHERE id=:thread_id;"""
    db.session.execute(sql_threads, {"thread_id": thread_id})
    sql_messages = (
        """UPDATE messages SET is_visible=FALSE WHERE thread_id=:thread_id;"""
    )
    db.session.execute(sql_messages, {"thread_id": thread_id})
    db.session.commit()
    return True

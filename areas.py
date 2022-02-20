from db import db
import users


def get_list():
    if users.user_is_admin():
        sql = """
            WITH join_table AS (
                SELECT ar.id, ar.name, ar.created_at, ar.user_id, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                    me.created_at AS created_at_message,
                    ar.is_visible area_vis, th.is_visible thread_vis, me.is_visible message_vis, ur.is_visible user_vis
                FROM areas ar 
                    JOIN users as ur ON ar.user_id=ur.id
                    LEFT JOIN threads th ON ar.id=th.area_id 
                    LEFT JOIN messages as me ON th.id=me.thread_id        
                )
            SELECT id, name, created_at, user_name, 
                COUNT(DISTINCT(CASE WHEN thread_vis=TRUE THEN thread_id END)) as count_threads, 
                COUNT(DISTINCT(CASE WHEN message_vis=TRUE THEN message_id END)) as count_messages, 
                max(CASE WHEN message_vis=TRUE THEN created_at_message END) AS created_at_message_max
            FROM join_table 
            WHERE area_vis=TRUE 
            GROUP BY id, name, created_at, user_name
            """
        result = db.session.execute(sql)
    else:
        sql = """
            WITH join_table_not_secret AS (
                SELECT ar.id, ar.name, ar.created_at, ar.user_id, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                    me.created_at AS created_at_message,
                    ar.is_visible area_vis, th.is_visible thread_vis, me.is_visible message_vis, ur.is_visible user_vis
                FROM areas ar
                    JOIN users as ur ON ar.user_id=ur.id
                    LEFT JOIN threads th ON ar.id=th.area_id 
                    LEFT JOIN messages as me ON th.id=me.thread_id
                    WHERE ar.is_secret=FALSE
                ),
            join_table_secret AS (
                SELECT ar.id, ar.name, ar.created_at, ar.user_id, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                    me.created_at AS created_at_message,
                    ar.is_visible area_vis, th.is_visible thread_vis, me.is_visible message_vis, ur.is_visible user_vis
                FROM users_areas usar 
                    LEFT JOIN areas ar ON usar.area_id=ar.id
                    JOIN users as ur ON ar.user_id=ur.id
                    LEFT JOIN threads th ON ar.id=th.area_id 
                    LEFT JOIN messages as me ON th.id=me.thread_id
                    WHERE ar.is_secret=TRUE AND usar.user_id=:user_id_current
                ),
            join_table_full AS (
                SELECT * FROM join_table_not_secret  
                UNION ALL 
                SELECT * FROM join_table_secret 
                )
            SELECT id, name, created_at, user_name, 
                COUNT(DISTINCT(CASE WHEN thread_vis=TRUE THEN thread_id END)) as count_threads, 
                COUNT(DISTINCT(CASE WHEN message_vis=TRUE THEN message_id END)) as count_messages, 
                max(CASE WHEN message_vis=TRUE THEN created_at_message END) AS created_at_message_max
            FROM join_table_full 
            WHERE area_vis=TRUE 
            GROUP BY id, name, created_at, user_name
            """
        result = db.session.execute(sql, {'user_id_current':users.user_id()})
    
    areas_list = result.fetchall()
    areas_list = [list(tup) for tup in areas_list]
    for area in areas_list:
        area[2] = area[2].strftime("%Y-%m-%d %H:%M:%S")
        area[-1] = 'Ei viestejä' if area[-1] is None else area[-1].strftime("%Y-%m-%d %H:%M:%S")
    return areas_list


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

def create_secret(area_name, user_id_list):
    user_id = users.user_id()
    if user_id == 0:
        return False
    #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
    sql = "INSERT INTO areas (user_id, name, created_at, is_secret, is_visible) VALUES (:user_id, :area_name, NOW(), TRUE, TRUE)"
    db.session.execute(sql, {"user_id":user_id, 'area_name': area_name})
    db.session.commit()
    sql_area_id = "SELECT id FROM areas ORDER BY id DESC LIMIT 1;"
    result = db.session.execute(sql_area_id)
    area_id = result.fetchone()[0]
    print(f"areas, create_secret, area_id: {area_id}")
    print(f"areas, create_secret, user_id_list: {user_id_list}")
    for user_id in user_id_list:
        print(f"areas, create_secret, in loop, user_id: {user_id}")
        sql_users_areas = "INSERT INTO users_areas (user_id, area_id) VALUES (:user_id, :area_id)"
        db.session.execute(sql_users_areas, {"user_id":int(user_id), 'area_id': area_id})
    db.session.commit()
    return True

def delete(area_id):
    sql_messages = """
        WITH deletable_threads AS (
            SELECT id from threads WHERE area_id=:area_id
            )
        UPDATE messages SET is_visible=FALSE WHERE thread_id IN (SELECT id FROM deletable_threads);
        """
    db.session.execute(sql_messages, {"area_id":area_id})
    sql_threads = """UPDATE threads SET is_visible=FALSE WHERE area_id=:area_id;"""
    db.session.execute(sql_threads, {"area_id":area_id})
    sql_areas = """UPDATE areas SET is_visible=FALSE WHERE id=:area_id;"""
    db.session.execute(sql_areas, {"area_id":area_id})
    db.session.commit()
    return True


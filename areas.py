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
    #sql = """SELECT A.name, U.name, A.created_at, A.id FROM areas A, users U WHERE A.user_id=U.id ORDER BY A.created_at"""
    sql = """
        WITH join_table AS (
            SELECT ar.id, ar.name, ar.created_at, ar.user_id, ur.name AS user_name, me.thread_id, me.id AS message_id, 
                me.created_at AS created_at_message from areas ar 
                JOIN users as ur ON ar.user_id=ur.id
                LEFT JOIN threads th ON ar.id=th.area_id 
                LEFT JOIN messages as me ON th.id=me.thread_id
                
            )
        SELECT id, name, created_at, user_name, COUNT(DISTINCT(thread_id)) as count_threads, 
            COUNT(DISTINCT(message_id)) as count_messages, max(created_at_message) AS created_at_message_max
        from join_table GROUP BY id, name, created_at, user_name
        """
    sql = """
        WITH join_table AS (
            SELECT ar.id, ar.name, ar.created_at, ar.user_id, th.id AS thread_id, me.id AS message_id, 
                me.created_at AS created_at_message,
                ar.is_visible area_vis, th.is_visible thread_vis, me.is_visible message_vis
                from areas ar
                LEFT JOIN threads th ON ar.id=th.area_id 
                LEFT JOIN messages as me ON th.id=me.thread_id
                WHERE th.is_visible=TRUE AND me.is_visible=TRUE
            ),
        users_join AS (
            SELECT ar.id, ur.id as user_id, ur.name as user_name 
            FROM areas ar 
            JOIN users as ur ON ar.user_id=ur.id
            )  
        
        SELECT ar.id, ar.name, ar.created_at, uj.user_name, COUNT(DISTINCT(jt.thread_id)) as count_threads, 
            COUNT(DISTINCT(jt.message_id)) as count_messages, max(jt.created_at_message) AS created_at_message_max
        from areas AS ar 
        LEFT JOIN join_table AS jt ON ar.id=jt.id
        LEFT JOIN users_join AS uj ON ar.id=uj.id
        WHERE ar.is_visible=TRUE
        GROUP BY ar.id, ar.name, ar.created_at, uj.user_name
        """
    sql =  """
        WITH join_table AS (
            SELECT ar.id, ar.name, ar.created_at, ar.user_id, ur.name AS user_name, th.id AS thread_id, me.id AS message_id, 
                me.created_at AS created_at_message,
                ar.is_visible area_vis, th.is_visible thread_vis, me.is_visible message_vis, ur.is_visible user_vis
                FROM areas ar 
                JOIN users as ur ON ar.user_id=ur.id
                LEFT JOIN threads th ON ar.id=th.area_id 
                LEFT JOIN messages as me ON th.id=me.thread_id        
            )
        SELECT id, name, created_at, user_name, COUNT(DISTINCT(CASE WHEN thread_vis=TRUE THEN thread_id END)) as count_threads, 
            COUNT(DISTINCT(CASE WHEN message_vis=TRUE THEN message_id END)) as count_messages, max(created_at_message) AS created_at_message_max
            FROM join_table GROUP BY id, name, created_at, user_name
        """
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

# def send(content):
#     user_id = users.user_id()
#     if user_id == 0:
#         return False
#     #sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (:content, :user_id, NOW())"
#     sql = "INSERT INTO messages (content, user_id, created_at) VALUES (:content, :user_id, NOW())"
#     db.session.execute(sql, {"content":content, "user_id":user_id})
#     db.session.commit()
#     return True

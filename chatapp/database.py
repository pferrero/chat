import sqlite3
import datetime

#DB_NAME = "file::memory:?cache=shared"
DB_NAME = "test.db"

### Crear tablas
#with open('modelotest.sql') as script:
#    connection = sqlite3.connect(DB_NAME)
#    connection.executescript(script.read())
#    connection.close()

def nuevo_usuario(user_name, user_pass):
    """
    Crea un nuevo usuario en la base de datos.
    :param user_name: El nombre de usuario
    :type user_name: str
    :param user_pass: La contraseña de usuario
    :type user_pass: str
    :return type: boolean
    """
    values = (user_name, user_pass)
    con = sqlite3.connect(DB_NAME)
    try:
        with con:
            con.execute("INSERT INTO usuario VALUES (NULL,?,?)", values)
    except sqlite3.IntegrityError:
        print(f"No se pudo agregar el usuario {user_name}")
        return False
    con.close()
    return True

def check_login(user_name, user_pass):
    """
    Verifica que el usuario exista y la contraseña sea correcta para
    hacer el login.
    :param user_name: El nombre de usuario
    :type user_name: str
    :param user_pass: La contraseña de usuario
    :type user_pass: str
    :return: boolean
    """
    con = sqlite3.connect(DB_NAME)
    with con:
        cur = con.execute("SELECT pass FROM usuario WHERE username = ?",
                         (user_name,))
        password = cur.fetchone()
    con.close()
    return password != None and password[0] == user_pass

def exists_user(username):
    """
    Checks if a user exists in the database.
    :param username: The username to check.
    :type username: str
    :return: bool
    """
    con = sqlite3.connect(DB_NAME)
    with con:
        cur = con.execute("SELECT 1 FROM usuario WHERE username = ?",
                          (username,))
        exists = cur.fetchone()
    con.close()
    return exists != None

def crear_mensaje(from_username, to_username, msg):
    """
    Crea un nuevo mensaje desde el usuario
    from_username con destinatario el usuario to_username
    y el mensaje msg.
    :param from_username: Usuario que envia el mensaje
    :type from_username: str
    :param to_username: Usuario que recibe el mensaje
    :type to_username: str
    :param msg: Mensaje
    :type msg: str
    """
    con = sqlite3.connect(DB_NAME)
    with con:
        con.execute("""
            INSERT INTO mensaje VALUES (NULL,
            (SELECT id_usuario FROM usuario WHERE username = ?),
            (SELECT id_usuario FROM usuario WHERE username = ?),
            ?,
            ?)
            """,
            (from_username, to_username, msg, datetime.datetime.now())
        )
    con.close()

def get_mensajes_from_to(from_username, to_username, from_datetime=None, to_datetime=None):
    """
    Devuelve todos los mensajes que envió from_username a to_username
    :param from_username: Usuario que envió los mensajes
    :type from_username: str
    :param to_username: Usuario que recibió los mensajes
    :type to_username: str
    :return: lista de mensajes
    """
    start_time = ""
    if from_datetime is not None:
        start_time = "AND fecha_hora > '" + str(from_datetime) + "'"
    end_time = ""
    if to_datetime is not None:
        end_time = "AND fecha_hora < '" + str(to_datetime) + "'"
    con = sqlite3.connect(DB_NAME)
    with con:
        res = con.execute(
            """
            SELECT f.username, t.username, m.msj, m.fecha_hora 
            FROM mensaje m, usuario f, usuario t 
            WHERE m.from_user = f.id_usuario 
            AND m.to_user = t.id_usuario 
            AND f.username = ? 
            AND t.username = ?
            {}
            {}
            """.format(start_time, end_time),
            (from_username, to_username)
        )
    messages = res.fetchall()
    con.close()
    return messages

def get_mensajes(user1, user2, from_datetime=None, to_datetime=None):
    """
    Devuelve todos los mensajes entre user1 y user2
    :param user1: Usuario 1
    :type user1: str
    :param user2: Usuario 2
    :type user2: str
    :return: Lista de mensajes
    """
    start_time = ""
    if from_datetime is not None:
        start_time = "AND fecha_hora > '" + str(from_datetime) + "'"
    end_time = ""
    if to_datetime is not None:
        end_time = "AND fecha_hora < '" + str(to_datetime) + "'"
    con = sqlite3.connect(DB_NAME)
    with con:
        res = con.execute(
            """
            SELECT f.username, t.username, m.msj, m.fecha_hora 
            FROM mensaje m, usuario f, usuario t 
            WHERE m.from_user = f.id_usuario 
            AND m.to_user = t.id_usuario 
            AND (f.username = ? AND t.username = ? OR f.username = ? AND t.username = ?)
            {}
            {}
            ORDER BY m.fecha_hora DESC
            """.format(start_time, end_time),
            (user1, user2, user2, user1)
        )
    messages = res.fetchall()
    con.close()
    return messages
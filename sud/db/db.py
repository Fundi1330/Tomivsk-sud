from sqlite3 import connect

con = connect('sud.db')
cur = con.cursor()

def init_db():
    cur.execute('''CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                discord VARCHAR NOT NULL UNIQUE
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS zayava(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(320) NOT NULL,
                    description VARCHAR(1500),
                    active BOOLEAN NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                );''')
    
def get_user(tag):
    user = cur.execute('SELECT * FROM user WHERE discord=?', [tag])
    return user.fetchone()



def add_user(tag):
    user = cur.execute('INSERT INTO user(discord) VALUES(?)', [tag])
    con.commit()
    return user.fetchone()

def get_zayavas_by_user(tag):
    user = cur.execute('SELECT * FROM user WHERE discord=?', [tag]).fetchone()
    
    zayavas = cur.execute('SELECT * FROM zayava WHERE user_id=?', [user[0]])
    return zayavas.fetchall()

def get_object_by_val(key, val, table):
    object = cur.execute(f'SELECT * FROM {table} WHERE {key}=?', [val])

    return object.fetchone()

def create_object(keys, values, table):
    object = cur.execute(f'INSERT INTO {table}{keys} VALUES{values}')
    con.commit()
    return object.fetchone()
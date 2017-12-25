import sqlite3

database_name = "test.db"
table_name = "table"


def init():
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    try:
        cursor.execute("""create table test
        (id integer primary key,
        file_name text,
        md5 text,
        part_id integer,
        source_id text,
        target_id text);""")
        connect.commit()
        connect.close()
        return True
    except:
        print("create table failed")
        return False

def add_file(file_name, md5, part_id, source_id, target_id):
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    cursor.execute("insert into test \
    (file_name, md5, part_id, source_id, target_id) \
    values (?, ?, ?, ?, ?)", (file_name, md5, part_id, source_id, target_id))
    connect.commit()
    connect.close()


def search_all():
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    data = cursor.execute("""select * from test""")
    connect.close()
    return data


def get_all_files(name):
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    data = cursor.execute("""select * from test where target_id = \'"""+name+"\'")
    connect.close()
    return data


def get_file_md5(name):
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    data = cursor.execute("select * from test where file_name = \'"+name+"\'")
    connect.close()
    for i in data:
        return i[2]

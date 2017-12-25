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


def search_all(ip):
    connect = sqlite3.connect(database_name)
    cursor = connect.cursor()
    data = cursor.execute("""select * from test""")
    res = []
    print(data)
    for row in data:
        tmp = ["", "", "", ""]
        tmp[0] = row[1]
        print(row)
        if row[5] == ip:
            tmp[2] = u"已下载"
        else:
            tmp[2] = u"未下载"
        res.append(tmp)
    connect.close() 
    return res


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
    for i in data:
        name = i[2]
        break
    connect.close()
    return name

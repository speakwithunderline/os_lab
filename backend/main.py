from backend.sock import *
from backend.database import *


def get_file_list(sk):
    data = search_all()
    ip = sk.myIP()
    res = []
    for row in data:
        tmp = {}
        tmp['name'] = row[1]
        if row[5] == ip:
            tmp['state'] = "yes"
        else:
            tmp['state'] = "no"
        res.append(tmp)
    return res


def download_file(sk, ip, file_name):
    md5 = get_file_md5(file_name)
    sk.getfile(ip, md5)


def push_file(sk, ip, file_name):
    my_ip = sk.myIP()
    sk.connect(ip)
    md5 = sk.send_file(ip, file_name)
    name = file_name.split("/")[-1]
    add_file(name, md5, 0, my_ip, ip)


if __name__ == "__main__":
    sk = Sock()
    ip = '192.168.1.137'

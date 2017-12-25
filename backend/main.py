# -*- coding: utf-8 -*-
from backend.sock import *
from backend.database import *

sk = Sock()
ip = '192.168.1.137'
# init()
def get_file_list(sk=sk):
    data = search_all()
    ip = sk.myIP()
    res = []
    print(data)
    for row in data:
        tmp = ["", "", "", ""]
        tmp[0] = row[1]
        if row[5] == ip:
            tmp[2] = u"已下载"
        else:
            tmp[2] = u"未下载"
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
    init()

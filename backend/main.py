# -*- coding: utf-8 -*-
from backend.sock import *
from backend.database import *

sk = Sock()
ip = '192.168.1.137'
sk.connect(ip)
# init()
def get_file_list(sk=sk):
    ip = sk.myIP()
    data = search_all(ip)
    return data


def download_file(file_name, sk=sk, ip=ip):
    md5 = get_file_md5(file_name)
    sk.getfile(ip, md5)


def push_file(file_name, sk=sk, ip=ip):
    my_ip = sk.myIP()
    md5 = sk.send_file(ip, file_name)
    name = file_name.split("/")[-1]
    add_file(name, md5, 0, my_ip, ip)
    res = {}
    res['msg'] = 'succeed'
    res['file_status'] = [name, u"下载", "", ""]
    return res


if __name__ == "__main__":
    pass


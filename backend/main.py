from backend.sock import *
from backend.database import *


def get_file_list():
    data = search_all()
    ip = myIP()
    res = []
    for row in data:
        tmp = {}
        tmp['name'] = row[1]
        if row[5] == ip:
            tmp['state'] =


def download_file(sk, ip, file_name):



def push_file(sk, ip, file_name):
    pass

if __name__ == "__main__":
    sk = Sock()
    ip = '192.168.1.137'

import socket
import hashlib
import queue
import threading
from backend.constants import *
import time
import os

def extend_one_second() :
    time.sleep(default_extend)

class Sock:
    status = {}
    queue = {}
    active = {}
    sk = socket.socket()

    @staticmethod
    def myIP():
        def val(ip):
            ip = [int(i) for i in ip.split('.')]
            return ((ip[0]*256+ip[1])*256+(256-ip[2]))*256+ip[3]
        ipList = socket.gethostbyname_ex(socket.gethostname())[2]
        return sorted(ipList, key=val, reverse=True)[0]

    def q_empty(self, ip):
        if ip not in self.queue.keys():
            self.queue[ip] = queue.Queue()
        return self.queue[ip].empty()

    def query_active(self, ip):
        if ip not in self.active.keys() :
            self.active[ip] = active_wait
        return self.active[ip]

    def lock_active(self, ip):
        while self.query_active(ip) == active_lock :
            if DEBUG:
                print(ip,'waiting for lock')
            extend_one_second()
        self.active[ip] = active_lock

    def check_active(self, ip):
        if self.query_active(ip) != active_lock:
            if self.q_empty(ip):
                self.active[ip] = active_wait
            else:
                self.active[ip] = active_active

    def unlock_active(self, ip):
        self.active[ip] = active_wait
        self.check_active(ip)

    def get(self, ip):
        while self.q_empty(ip):
            if DEBUG:
                print('Waiting for message from IP =', ip)
            extend_one_second()
        r = self.queue[ip].get()
        print(r)
        self.check_active(ip)
        return r

    def put(self, ip, message):
        if ip not in self.queue.keys():
            self.queue[ip] = queue.Queue()
        self.queue[ip].put(message)
        self.check_active(ip)

    def hb(self, ip):
        if DEBUG:
            print('Get heartbeat from IP =', ip)
        if ip not in self.status.keys():
            self.status[ip] = time.time()
        self.status[ip] = time.time()

    def socket_process(self):
        while True:
            self.sk.listen(default_time_out)
            try:
                skt, address = self.sk.accept()
                data = skt.recv(default_size)
                if data == heartbeat:
                    self.hb(address[0])
                else:
                    self.put(address[0], data)
            except:
                pass
            extend_one_second()

    @staticmethod
    def send(ip, message):
        if DEBUG:
            print('Send', message, 'to', ip)
        while True:
            try:
                skt = socket.socket()
                skt.connect((ip, default_obj_port))
                skt.sendall(message)
                break
            except:
                if DEBUG:
                    print('Send ERROR!')
            extend_one_second()

    def connect (self, ip):
        self.send(ip, heartbeat)
        self.hb(ip)

    def heart_beat(self):
        while True:
            time.sleep(default_time_space)
            for ip in self.status.keys():
                self.send(ip, heartbeat)

    def __init__(self):
        self.sk.bind((self.myIP(), default_port))
        t = threading.Thread(target=self.socket_process)
        t.setDaemon(True)
        t.start()
        t = threading.Thread(target=self.heart_beat)
        t.setDaemon(True)
        t.start()
        if DEBUG:
            print('Initialized. IP =', self.myIP(), ', Port =', default_port)

    def send_file(self, ip, filename):
        file = open(filename, 'rb')
        data = file.read()
        file.close()

        md5 = hashlib.md5(data).digest()
        n = (len(data) + default_size - 1) // default_size

        if DEBUG:
            print('Send file :', data, ', md5 =', md5, ', cnt =', n, ', IP =', ip)

        self.lock_active(ip)
        while True:
            if DEBUG:
                print('Send begin:')
            try:
                self.send(ip, send_begin)
                self.send(ip, md5)
                self.send(ip, bytes(str(n), encoding=char_set))
                for i in range(n) :
                    self.send(ip, data[i*default_size:(i+1)*default_size])

                self.send(ip, send_end)

                recv = self.get(ip)
                if recv == accepted:
                    break
            except:
                if DEBUG:
                    print('Send file error. Resend.')
            extend_one_second()
        self.unlock_active(ip)
        return hashlib.md5(data).hexdigest()

    def pop_file(self, ip):
        while True:
            tmp = self.get(ip)
            if tmp == send_end :
                break

    def recv_file(self, ip):
        if DEBUG:
            print('Recv file. IP =', ip)
        self.lock_active(ip)
        while True:
            try:
                md5 = self.get(ip)
                if md5 == send_begin:
                    md5 = self.get(ip)
                if DEBUG:
                    print('Recv file, md5 =', md5)

                data = []
                n = int(str(self.get(ip), char_set))
                while len(data) < n:
                    kw = self.get(ip)
                    data.append(kw)

                kw = self.get(ip)
                if kw != send_end :
                    self.pop_file(ip)
                    raise IOError

                data = b''.join(data)

                if DEBUG:
                    print('Recv data :', data)

                if md5 != hashlib.md5(data).digest() :
                    if DEBUG:
                        print('Wrong hash! md5 :', md5, hashlib.md5(data).digest())
                    raise IOError

                md5 = hashlib.md5(data).hexdigest()

                try:
                    if not os.path.exists(work_dir):
                        os.mkdir(work_dir)
                    save_file = open(work_dir+'\\'+md5, 'wb')
                    save_file.write(data)
                    save_file.close()
                except:
                    if DEBUG:
                        print('Cannot save in file! filename =', work_dir+'\\'+md5)
                    raise IOError

                self.send(ip, accepted)
                break
            except:
                self.send(ip, wrong_answer)
            extend_one_second()
        self.unlock_active(ip)
        print('recv')
        return md5

    def getfile(self, ip, md5):
        self.send(ip, want_file)
        self.send(ip, bytes(work_dir+'\\'+md5, encoding=char_set))
        return self.recv_file(ip)

    def process_message(self, ip):
        try:
            kw = self.get(ip)
            if DEBUG:
                print('Get', kw, 'From', ip)
            if kw == send_begin:
                self.recv_file(ip)
            elif kw == want_file:
                md5 = str(self.get(ip), encoding=char_set)
                if DEBUG:
                    print('Wanted file :', md5)
                self.send_file(ip, md5)
        except:
            pass

    def server(self):
        while True:
            for ip in self.status.keys():
                if self.query_active(ip) == active_active:
                    self.process_message(ip)
            extend_one_second()


if __name__ == '__main__':
    sk = Sock()
    ip = '192.168.1.137'
    sk.connect(ip)
    md5 = sk.send_file(ip, 'a.txt')
    sk.getfile(ip, md5)

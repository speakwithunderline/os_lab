import socket
import hashlib
import queue
import threading
from .constants import *
import time

def extend_one_second() :
    time.sleep(default_extend)

class Sock:
    status = {}
    queue = {}
    active = {}
    sk = socket.socket()

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
        while self.query_active(ip) != active_active:
            time.sleep(default_extend)
        r = self.queue[ip].get()
        self.check_active(ip)
        return r

    def put(self, ip, message):
        if ip not in self.queue.keys():
            self.queue[ip] = queue.Queue()
        self.queue[ip].put(message)
        self.check_active(ip)

    def hb(self, ip):
        if ip not in self.status.keys():
            self.status[ip] = time.time()
        self.status[ip] = time.time()

    def socket_process(self):
        while True:
            extend_one_second()
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

    @staticmethod
    def send(ip, message):
        while True:
            extend_one_second()
            try:
                skt = socket.socket()
                skt.connect((ip, default_obj_port))
                skt.sendall(message)
                break
            except:
                pass

    def heart_beat(self):
        while True:
            time.sleep(default_time_space)
            for ip in self.status.keys():
                self.send(ip, heartbeat)

    def __init__(self):
        self.sk.bind((socket.gethostbyname(socket.gethostname()), default_port))
        t = threading.Thread(target=self.socket_process)
        t.setDaemon(True)
        t.start()
        t = threading.Thread(target=self.heart_beat)
        t.setDaemon(True)
        t.start()

    def send_file(self, ip, filename):
        file = open(filename, 'rb')
        data = file.read()
        file.close()

        md5 = hashlib.md5(data).digest()
        n = (len(data) + default_size - 1) // default_size

        self.lock_active(ip)
        while True:
            extend_one_second()
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
                pass
        self.unlock_active(ip)
        return hashlib.md5(data).hexdigest()

    def pop_file(self, ip):
        while True:
            tmp = self.get(ip)
            if tmp == send_end :
                break

    def recv_file(self, ip):
        self.lock_active(ip)
        while True:
            extend_one_second()
            try:
                kw = self.get(ip)
                if kw != send_begin :
                    raise IOError
                md5 = self.get(ip)

                data = []
                n = int(str(self.get(ip), char_set))
                for i in range(n) :
                    data.append(self.get(ip))

                kw = self.get(ip)
                if kw != send_end :
                    self.pop_file(ip)
                    raise IOError

                data = b''.join(data)
                if md5 != hashlib.md5(data).digest() :
                    raise IOError

                md5 = hashlib.md5(data).hexdigest()

                save_file = open(work_dir+'\\'+md5, 'wb')
                save_file.write(data)
                save_file.close()

                self.send(ip, accepted)
                break
            except:
                self.send(ip, wrong_answer)
        self.unlock_active(ip)
        return md5

    def getfile(self, ip, md5):
        self.send(ip, want_file)
        self.send(ip, bytes(md5, encoding=char_set))
        return self.recv_file(ip)

    def process_message(self, ip):
        kw = self.get(ip)
        if kw == want_file:
            md5 = str(self.get(ip), encoding=char_set)
            self.send_file(ip, md5)

    def server(self):
        while True:
            extend_one_second()
            for ip in self.status.keys():
                if self.query_active(ip):
                    t = threading.Thread(target=self.process_message, args=(ip))
                    t.setDaemon(True)
                    t.start()


if __name__ == '__main__':
    sk = Sock()
    sk.server()

if __name__ == '__main__':
    sk = Sock()
    ip = '192.168.1.137'
    md5 = sk.send_file(ip, 'a.txt')
    sk.getfile(ip, md5)
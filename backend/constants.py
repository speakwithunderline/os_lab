
char_set = 'utf-8'
work_dir = '\data'

#Networks:
default_port = 8080
default_obj_port = 8080

#Clocks:
default_time_out = 20
default_time_space = 5

default_size = 1024

#Actives:
active_wait = 0
active_lock = -1
active_active = 1

#Keywords:
heartbeat = bytes('heartbeat', encoding=char_set)

send_begin = bytes('send_begin', encoding=char_set)
send_end = bytes('send_end', encoding=char_set)
accepted = bytes('Accepted', encoding=char_set)
wrong_answer = bytes('WrongAnswer', encoding=char_set)
want_file = bytes('give me a file', encoding=char_set)
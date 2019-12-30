import socket
import threading
import os
import sys
import time
from file import *
from queue import Queue

class TorServer:
    def __init__(self, port):
        try:
            self.host = ''
            self.port = int(port)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.users = []
            self.list_commands = ['list', 'search', 'show', 'upload', 'download']
            self.response = ['This command does not exist, rewrite', 'end-ok']
            self.NUMBER_OF_THREADS = 2 # ?
            self.JOB_NUMBER = [1, 2] # ?
            self.queue = Queue()

        except socket.error as msg:
            print('Socket creation error: ' + str(msg))
                   

    def bind_socket(self):
        try:
            print('Binding the Port: ' + str(self.port))
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
        except socket.error as msg:
            print('Socket binding error: ' + str(msg) + '\n' + 'Retrying...')
            self.bind_socket()

    def accept_connections(self):
        for i in self.users:
            i.close()
  
        del self.users[:]
    
        while True:
            try:
                conn, address = self.server_socket.accept()
                self.server_socket.setblocking(1)  # prevents timeout
                self.users.append(address)

                client_ip = address[0]
                print('Client {} is online now'.format(client_ip))
                
                x = threading.Thread(target=self.client_thread, args=(conn, address[0]), daemon=True)
                x.start()

            except:
                print('Error accepting connections')

    def commands(self):
        while True:
            str_input = input()
            if (str_input == 'clear'):
                os.system('clear')
            elif str_input == 'list':
                self.list()
            else:
                print(str_input)    

    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.bind_socket()
                self.accept_connections()
            if x == 2:
                self.commands()

            self.queue.task_done()

    def create_threads(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work, daemon=True)
            t.start()

    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)
        self.queue.join()

    # Client-Server Communication:
    def client_command(connself, conn):
        str_input = conn.recv(2048)
        str_input = str_input.rstrip()
        str_input = str_input.decode()

        return str_input
    
    def server_client_communication(self, conn, error):
        # wait for 300 milliseconds
        time.sleep(.3) 
        
        # then send the command
        if error:
            conn.send(self.response[0].encode())    
        else:
            conn.send(self.response[1].encode())

    # Thread for a client (one new thread for each one client)
    # input_commands[0] = search / show / upload / download
    # input_commands[1] = .txt / video.mp4 / musica.mp3
    def client_thread(self, conn, client_ip):
        while True:
            input_commands = self.client_command(conn)
            input_commands = input_commands.split(' ')

            if input_commands[0] == 'exit':
                flag = 0
                for i in enumerate(self.users):
                    user_ip = i[1][0]
                    index = i[0]
                    if user_ip == client_ip:
                        print('Client {} is offline now'.format(client_ip))
                        flag = 1
                        del self.users[index]
                        break
                if flag == 1:
                    break
            else:
                if input_commands[0] in self.list_commands:
                    self.switcher(conn, input_commands)
                else:
                    conn.send(self.response[1].encode())


    # Switchers of commands
    def switcher(self, conn, input_commands):
        size = len(input_commands)

        method_name = input_commands[0]
        method = getattr(self, method_name)

        if size == 1:    
            new_t = threading.Thread(target=method, args=(conn,), daemon=True)
            new_t.start()
        elif size == 2:
            input_file = input_commands[1]
            new_t = threading.Thread(target=method, args=(conn, input_file), daemon=True)
            new_t.start()
        else:
            conn.send(response[0].encode())
        error = 0
        self.server_client_communication(conn, error)


    # Actions: List, Search, Show, Upload, Download
    def list(self):
        results = ''

        size = str(len(self.users))
        for i, conn in enumerate(self.users):
            results = str(self.users[i][0]) + '\t' + str(self.users[i][1]) + '\n'

        print('[ Clients: ' + size + ' ]\nIP Address\tPort\n' + results)

    def search(self, conn, input_file):
        str_file = ''
        dir_path = os.path.dirname(os.path.realpath(__name__))
        dir_path = dir_path + '/files'
        print('dir_path: ' + dir_path)

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                filename = file.name
                if filename.find(input_file) != -1:
                    file_info = file.stat()
                    
                    new_file = File()
                    new_file.update_file(filename, file_info.st_size, file_info.st_mtime)
                    str_file += str(new_file)
        
        # str_file = files.
        # size = str(sys.getsizeof(str_file))
        # print("size: ", sys.getsizeof(str_file))
        
        conn.send(str_file.encode())

        error = 0
        self.server_client_communication(conn, error)
    
    def show(self, conn):
        str_file = ''
        dir_path = os.path.dirname(os.path.realpath(__name__))
        dir_path = dir_path + '/files'

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                file_info = file.stat()

                new_file = File()
                new_file.update_file(file.name, file_info.st_size, file_info.st_mtime)
                str_file += str(new_file)

        conn.send(str_file.encode())

        error = 0
        self.server_client_communication(conn, error)
      
    # def upload(self, temp):
        # print('uploading')

    # def download(self, temp):
        # print('downloading')

    
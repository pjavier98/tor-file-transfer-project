import socket
import threading
import os
import sys
import time
from queue import Queue
from file import *

class TorServer:
    def __init__(self, port):
        try:
            self.host = ''
            self.port = int(port)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.is_server_closed = False
            self.users = []
            self.list_commands = ['search', 'show', 'upload', 'download']
            self.response = ['This command does not exist, rewrite', 'end', 'off', 'ok']
            self.NUMBER_OF_THREADS = 2
            self.JOB_NUMBER = [1, 2]
            self.queue = Queue()

        except socket.error as msg:
            print('Socket creation error: ' + str(msg))
                   
    # Tor-Server
    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.bind_socket()
                self.accept_connections()
            if x == 2:
                command = self.commands()

            self.queue.task_done()

    def create_threads(self):
        for _ in range(self.NUMBER_OF_THREADS):
            t = threading.Thread(target=self.work, daemon=True)
            t.start()

    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)
        self.queue.join()

    def bind_socket(self):
        try:
            print('Binding the Port: ' + str(self.port))
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
        except socket.error as msg:
            print('Socket binding error: ' + str(msg) + '\n' + 'Retrying...')
            self.bind_socket()

    def accept_connections(self):
        while True:
            try:
                conn, address = self.server_socket.accept()
                self.server_socket.setblocking(1)  # prevents timeout
                self.users.append(address)

                client_ip = address[0]
                print('Client {} is online now'.format(client_ip), end='\n\n')
                
                x = threading.Thread(target=self.client_thread, args=(conn, address[0]), daemon=True)
                x.start()
            except:
                if self.is_server_closed:
                    print('Server connection was closed')
                else:
                    print('Error accepting connections')
                break

    def close_server_connection(self):
        users = len(self.users)
        if users == 0:
            self.is_server_closed = True
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()
            return 1
        else:
            print('There are {} people connected, you cannot close the connection'.format(users))
            return 0
    
    def commands(self):
        while True:
            str_input = input('tor >> ')
            if (str_input == 'clear'):
                os.system('clear')
            elif str_input == 'list':
                self.list()
            elif str_input == 'exit':
                if (self.close_server_connection()):
                    break
            else:
                print(self.response[0], end='\n\n')

    def list(self):
        results = ''

        size = str(len(self.users))
        for i, conn in enumerate(self.users):
            results = str(self.users[i][0]) + '\t' + str(self.users[i][1]) + '\n'

        print('[ Clients: ' + size + ' ]\nIP Address\tPort\n' + results)
  
    # Client-Server Communication:
    def client_command(self, conn):
        str_input = conn.recv(4096)
        str_input = str_input.rstrip()
        str_input = str_input.decode()
        return str_input

    def server_client_communication(self, conn, error_num):
        # wait for 300 milliseconds
        time.sleep(.3) 
        
        # then send the command
        conn.send(self.response[error_num].encode())    

    def finalize_client_connection(self, conn, client_ip):
        end = 0
        for i in enumerate(self.users):
            user_ip = i[1][0]
            index = i[0]
            if user_ip == client_ip:
                print('Client {} is offline now'.format(client_ip), end='\n\n')
                end = 1
                del self.users[index]
                break
        return end

    def commands_rules(self, input_commands):
        command = input_commands[0]
        command_size = len(input_commands)
        command_in_list = False
        accept_command = False

        if command in self.list_commands:
            command_in_list = True
        
        if command == 'show':
            accept_command = True
        elif command == 'search' or command == 'upload' or command == 'download' and command_size == 2:
            accept_command = True

        return (command_in_list and accept_command)

    # Thread for a client (one new thread for each one client)
    # input_commands[0] = search / show / upload / download
    # input_commands[1] = .txt / video.mp4 / musica.mp3
    def client_thread(self, conn, client_ip):
        while True:
            input_commands = self.client_command(conn)
            input_commands = input_commands.split(' ')
            
            if input_commands[0] == 'exit':
                if (self.finalize_client_connection(conn, client_ip)):
                    break
            else:
                accept_command = self.commands_rules(input_commands) 
                if accept_command:
                    conn.send(self.response[3].encode())
                    self.switcher(conn, input_commands)
                else:
                    conn.send(self.response[0].encode())

    # Switchers of commands
    def switcher(self, conn, input_commands):
        method_name = input_commands[0]
        method = getattr(self, method_name)
        
        if method_name == 'show':
            new_t = threading.Thread(target=method, args=(conn,), daemon=True)
            new_t.start()
        else:
            input_file = input_commands[1]
            new_t = threading.Thread(target=method, args=(conn, input_file), daemon=True)
            new_t.start()

    # Actions: Search, Show, Upload, Download
    def send_search_file(self, conn, str_search_file, input_file):
        if len(str_search_file) > 0:
            conn.sendall(str_search_file.encode())
        else:
            if input_file == 'no-input-file':
                str_search_file = 'There are not files to search'
            else:
                str_search_file = 'Not found file with the string/substring: [' + input_file + ']'
            conn.sendall(str_search_file.encode())
        error_num = 1
        self.server_client_communication(conn, error_num)

    def search(self, conn, input_file):
        str_file = ''
        dir_path = os.path.dirname(os.path.realpath(__name__))
        dir_path = dir_path + '/files'
        # print('dir_path: ' + dir_path)

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                filename = file.name
                if filename.find(input_file) != -1:
                    file_info = file.stat()
                    
                    new_file = File()
                    new_file.update_file(filename, file_info.st_size, file_info.st_mtime)
                    str_file += str(new_file)
        self.send_search_file(conn, str_file, input_file)
    
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
        self.send_search_file(conn, str_file, 'no-input-file')
         
    # def upload(self, temp):
        # print('uploading')

    # def download(self, temp):
        # print('downloading')
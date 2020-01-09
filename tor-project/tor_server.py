import socket
import threading
import os
import sys
import time
from queue import Queue
from file import *
from time import sleep
from tqdm import tqdm

class TorServer:

    def __init__(self):
        try:
            self.alive = 1
            self.host = ''
            self.port = ''
            self.users = []
            self.is_server_closed = False
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.list_commands = ['search', 'show', 'upload', 'download']
            self.response = ['This command does not exist, rewrite', 'end', 'ok', 'found', 'Not found file']
            self.NUMBER_OF_THREADS = 2
            self.JOB_NUMBER = [1, 2]
            self.queue = Queue()
        except socket.error as msg:
            print('Socket creation error: ' + str(msg))
    
    def create_folder(self):
        try:
            folder = 'tor_files'
            os.mkdir(folder)
            print("Directory " + folder + " created with success") 
        except FileExistsError:
            print("Directory " + folder + " already exists")
    
    def switch_dir(self):
        os.chdir('tor_files')

    # Tor-Server
    def work(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.bind_socket()
                self.create_folder()
                self.switch_dir()
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

    def bind_socket(self):
        while True:
            try:
                self.port = int(input('Enter the port to launch Tor-Server: '))
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen()
                print('Binding the Port: ' + str(self.port))
                break
            except ValueError as msg:
                print(msg)
            except OSError as msg:
                print(msg)
            except socket.error as msg:
                print('Socket binding error: ' + str(msg) + '\n' + 'Retrying...')

    def accept_connections(self):
        while True:
            try:
                conn, address = self.server_socket.accept()
                self.server_socket.setblocking(1)  # prevents timeout
                self.users.append(address)

                print('Client {} is online now'.format(address), end='\n\n')
                x = threading.Thread(target=self.client_thread, args=(conn, address), daemon=True)
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

    def server_client_communication(self, conn, index):
        # wait for 100 milliseconds
        time.sleep(.3) 
        
        # then send the command
        conn.send(self.response[index].encode())    

    def finalize_client_connection(self, conn, address):
        end = 0
        for i in enumerate(self.users):
            user_ip = i[1][0]
            user_port = i[1][1]
            index = i[0]
            if user_ip == address[0] and user_port == address[1]:
                print('Client {} is offline now'.format(address), end='\n\n')
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
    def client_thread(self, conn, address):
        while True:
            input_commands = self.client_command(conn)
            input_commands = input_commands.split(' ')
            
            if input_commands[0] == 'exit':
                if (self.finalize_client_connection(conn, address)):
                    break
            else:
                accept_command = self.commands_rules(input_commands) 
                if accept_command:
                    self.server_client_communication(conn, 2)

                    # self.switcher(conn, input_commands)
                    action_thread = threading.Thread(target=self.switcher, args=(conn, address, input_commands), daemon=True)
                    action_thread.start()
                    
                    action_thread.join()

                else:
                    self.server_client_communication(conn, 0)

    # Switchers of commands
    def switcher(self, conn, address, input_commands):
        method_name = input_commands[0]
        method = getattr(self, method_name)
        
        if method_name == 'show':
            return method(conn, address)
        else:
            filename = input_commands[1]
            return method(conn, address, filename)

    # Actions: Search, Show, Upload, Download
    def send_search_file(self, conn, address, str_search_file, filename):
        if len(str_search_file) > 0:
            conn.sendall(str_search_file.encode())
        else:
            if filename == 'no-input-file':
                str_search_file = 'There are not files to search'
            else:
                str_search_file = 'Not found file with the string/substring: [' + filename + ']'
            conn.sendall(str_search_file.encode())
        self.server_client_communication(conn, 1)
        print('Search was made successfully by client: {}'.format(address))

    def search(self, conn, address, filename):
        dir_path = os.path.dirname(os.path.realpath(__name__))
        str_file = ''

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                file_name = file.name
                if file_name.find(filename) != -1:
                    file_info = file.stat()
                    
                    new_file = File()
                    new_file.update_file(file_name, file_info.st_size, file_info.st_mtime)
                    str_file += str(new_file)
        self.send_search_file(conn, address, str_file, filename)
    
    def show(self, conn, address):
        dir_path = os.path.dirname(os.path.realpath(__name__))
        str_file = ''

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                filename = file.name
                  
                file_info = file.stat()
                    
                new_file = File()
                new_file.update_file(filename, file_info.st_size, file_info.st_mtime)
                str_file += str(new_file)
        self.send_search_file(conn, address, str_file, 'no-input-file')
         
    def upload(self, conn, address, filename):
        founded = self.client_command(conn)

        if (response == 'founded'):
            print('File "{}" was sent by {}'.format(filename, address))
            print('Downloading ...')
            dir_path = os.path.dirname(os.path.realpath(__name__))
            filesize = int(self.client_command(conn))
            pbar = tqdm(total=filesize, unit="KB")
            size = 0

            with open(os.path.join(dir_path, filename), "wb") as new_file:
                while size < filesize:
                    response = conn.recv(4096)
                    size += len(response)
                    pbar.update(len(response))
                    
                    new_file.write(response)
                pbar.close()
            new_file.close()

            print('File "{}" was successfully uploaded by client: {}'.format(filename, address))
        
    def download(self, conn, address, filename):
        dir_path = os.path.dirname(os.path.realpath(__name__))
        founded = 0
        print('File "{}" was sent request by {}'.format(filename, address))
        print('Sending...')
        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                if file.name == filename:
                    self.server_client_communication(conn, 3)
                    download_file = open(file, "rb")
                    size = file.stat().st_size

                    # Send the size of the file
                    conn.send(str(size).encode())
                    # Wait for 100 miliseconds to send the next command
                    time.sleep(0.3)
                    # Send the bytes of the file
                    conn.sendall(download_file.read(size))

                    download_file.close()
                    founded = 1
                    break

        if (founded):
            print('File "{}" was sent successfully to {}'.format(filename, address))
        else:
            self.server_client_communication(conn, 4)
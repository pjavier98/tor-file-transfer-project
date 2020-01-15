import socket
import os
import time
from tqdm import tqdm

class Client:
      
    def __init__(self):
        self.host = ''
        self.port = ''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def create_dir(self):
        try:
            folder = 'client_files'
            upload = 'upload'
            download = 'download'
            os.mkdir(folder)
            os.mkdir(folder + '/' + upload)
            os.mkdir(folder + '/' + download)
            print("Directories [" + folder + ', ' + upload +  ', ' + download + "] created with success") 
        except FileExistsError:
            print("Directory " + folder + " already exists")

    def switch_dir(self):
        os.chdir('client_files')

    def iniciate_connection(self):
        print('Enter the host and the port application to connect')
        
        while True:
            try:
                self.host = input('host: ')
                self.port = int(input('port: '))
                self.server_socket.connect((self.host, self.port))
                print('\nConnection was established with success\n')
                return True
            except ConnectionRefusedError as msg:
                print(msg)
            except ValueError as msg:
                print(msg)
         
    def close_client_connection(self):
        print('Connection with the server was closed')
        self.server_socket.close()

    def server_command(self):
        str_input = self.server_socket.recv(4096)
        str_input = str_input.rstrip()
        str_input = str_input.decode()

        return str_input

    def server_client_communication(self, response):
        # Finalize the last command
        if (response == 'end' or not response):
            return True
        else:
            return False
    
    # input_commands[0] = search | show | upload | download
    # input_commands[1] = .txt | video.mp4 | musica.mp3 | substring
    def send_commands(self):
        while True:
            try:
                first_command = '\nSelect one of the commands below:\n'
                second_command = '[*] show\n[*] search <file>\n[*] upload <file>\n[*] download <file>\n[*] exit\n'

                input_commands = input(first_command + second_command + '\n>> ')
                aux_input = input_commands.split(' ')
                if aux_input[0] == 'exit':
                    self.server_socket.sendall(input_commands.encode())
                    self.close_client_connection()
                    break
                elif int(len(input_commands)) < 100:
                    self.server_socket.sendall(input_commands.encode())
                    input_commands = input_commands.split(' ')
                    response = self.server_command()
                    
                    if (response == 'ok'):
                        self.switcher(input_commands)
                    else:
                        print(response)
                else:
                    print('Command not recognized')
            except KeyboardInterrupt:
                print('\nThis command does not exist, rewrite')
            
    def switcher(self, input_commands):
        method_name = input_commands[0]
        method = getattr(self, method_name)
        
        if method_name == 'show' or method_name == 'search':
            return method()
        else:
            filename = input_commands[1]
            return method(filename)

    def receive_search_file(self):
        str_output = ''
        while True:
            response = self.server_command()

            if (self.server_client_communication(response)):
                break
            str_output += response
        return str_output
    
    # show (show all files)
    def show(self):
        str_files = self.receive_search_file()
        print(str_files)
        
    # search [ .txt | .png | .mp4 | .pdf ]
    def search(self):
        str_files = self.receive_search_file()
        print(str_files)

    def upload(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__name__)) + '/upload'
        founded = 0

        with os.scandir(dir_path) as dir_contents:
            for file in dir_contents:
                if file.name == filename:
                    upload_file = open(file, "rb")
                    size = file.stat().st_size

                    # Send the command that found the file
                    file_founded = 'founded'
                    self.server_socket.send(file_founded.encode())
                    # Wait for 100 miliseconds to send the next command
                    time.sleep(0.3)
                    # Send the size of the file
                    self.server_socket.send(str(size).encode())
                    # Wait for 100 miliseconds to send the next command
                    time.sleep(0.3)
                    # Send the bytes of the file
                    self.server_socket.sendall(upload_file.read(size))
                    
                    upload_file.close()
                    founded = 1
                    break
        
        if (founded):
            print('File "' + filename + '" was sent successfully', end='\n\n')
        else:
            file_founded = 'not founded'
            self.server_socket.send(file_founded.encode())
            print('Not found file: ' + filename)
        
    def download(self, filename):
        response = self.server_command()

        if response == 'found':
            print('Downloading...')
            dir_path = os.path.dirname(os.path.realpath(__name__)) + '/download'
            filesize = int(self.server_command())
            pbar = tqdm(total=filesize, unit="KB")
            size = 0

            with open(os.path.join(dir_path, filename), "wb") as new_file:
                while size < filesize:
                    response = self.server_socket.recv(4096)
                    
                    time.sleep(0.1)
                    size += len(response)
                    pbar.update(len(response))
                    
                    new_file.write(response)
                pbar.close()
            new_file.close()

            print('File "' + filename + '" was successfully downloaded')
        else:
            print(response)
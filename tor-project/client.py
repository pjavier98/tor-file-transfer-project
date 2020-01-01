import socket

class Client:
      
    def __init__(self):
        self.host = ''
        self.port = ''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def iniciate_connection(self, host='', port=15096):
        self.client_socket.connect((host, port))
    
    def close_client_connection(self):
        print('Connection with the server was closed')
        self.client_socket.close()

    def server_command(self):
        str_input = self.client_socket.recv(4096)
        str_input = str_input.rstrip()
        str_input = str_input.decode()

        return str_input

    def server_client_communication(self, response):
        # Finalize the last command
        if (response == 'end' or not response):
            return True
        else:
            return False
    
    # input_commands[0] = search / show / upload / download
    # input_commands[1] = .txt / video.mp4 / musica.mp3
    def send_commands(self):
        while True:
            try:
                first_command = '\nSelect one of the commands below:\n'
                second_command = '[*] Show\n' + '[*] Search <file>\n' + '[*] Upload <file>\n' + '[*] Download <file>\n' + '[*] Exit\n'

                input_commands = input(first_command + second_command + '\n>> ')
                aux_input = input_commands.split(' ')
                if aux_input[0] == 'exit':
                    self.client_socket.sendall(input_commands.encode())
                    self.close_client_connection()
                    break
                elif int(len(input_commands)) < 50:
                    self.client_socket.sendall(input_commands.encode())
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
        return method()

    def receive_search_file(self):
        str_output = ''
        while True:
            response = self.server_command()

            if (self.server_client_communication(response)):
                # end
                break
            str_output += response
        return str_output
    
    # show (show all files)
    def show(self):
        str_files = self.receive_search_file()
        print(str_files)
        
    # search .txt
    def search(self):
        str_files = self.receive_search_file()
        print(str_files)

    # def upload(self):

    # def download(self):  
                
client = Client()
client.iniciate_connection()
client.send_commands()
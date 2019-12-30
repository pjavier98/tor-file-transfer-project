import socket

class Client:
      
    def __init__(self):
        self.host = ''
        self.port = ''
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.list_commands = ['list', 'search', 'show', 'upload', 'download', 'exit']
    
    def iniciate_connection(self, host='', port=15007):
        self.client_socket.connect((host, port))
    
    def finalize_connection(self):
        self.client_socket.close()
        print('Connection with the server was closed')

    def server_command(self):
        str_input = self.client_socket.recv(2048)
        str_input = str_input.rstrip()
        str_input = str_input.decode()

        return str_input

    def server_client_communication(self, response):
        # Finalize the last command
        if (response == 'end-ok' or not response):
            return True
        else:
            return False

    # input_commands[0] = search / show / upload / download
    # input_commands[1] = .txt / video.mp4 / musica.mp3
    def send_commands(self):
        while True:
            first_command = '\nSelect one of the commands below:\n'
            second_command = '[*] List\n' + '[*] Show\n' + '[*] Search <file>\n' + '[*] Upload <file>\n' + '[*] Download <file>\n' + '[*] Exit\n'

            str_input = input(first_command + second_command + '\n>> ')
            input_commands = str_input.split(' ')

            if input_commands[0] in self.list_commands:
                if (input_commands[0] == 'exit'):
                    self.client_socket.send(input_commands[0].encode())
                    # send a command to the server to delete the connection
                    self.finalize_connection()
                    break
                else:
                    self.switcher(input_commands)
            else:
                print('This command does not exist, rewrite\n')
            
    def switcher(self, input_commands):
        size = len(input_commands)

        method_name = input_commands[0]
        method = getattr(self, method_name)

        # No client threads required
        if size == 1:
            return method(input_commands[0])
        elif size == 2:
            return method(input_commands)
        else:
            response = self.server_command()
            print(response)

    # show (show all files)
    def show(self, command):
        self.client_socket.send(command.encode())

        while True:
            response = self.server_command()

            if (self.server_client_communication(response)):
                # end-ok
                print(response)
                break
            print(response)
    
    
    # search .txt
    def search(self, input_commands):
        
        command = input_commands[0] + ' ' + input_commands[1]

        self.client_socket.send(command.encode())

        while True:
            response = self.server_command()

            if (self.server_client_communication(response)):
                # end-ok
                print(response)
                break
            print(response)
    
    


    # def upload(self):

    # def download(self):  
                
        


client = Client()
client.iniciate_connection()
client.send_commands()
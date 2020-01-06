from client import *

def create_client():
    client = Client()
    if (client.iniciate_connection()):
        client.create_dir()
        client.switch_dir()
        client.send_commands()

create_client()
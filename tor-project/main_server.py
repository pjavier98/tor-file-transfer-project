from tor_server import *

def create_tor_server():
    try:
        tor = TorServer()
        tor.create_threads()
        tor.create_jobs() 
    except ValueError as msg:
        print(msg)
        create_tor_server()

create_tor_server()
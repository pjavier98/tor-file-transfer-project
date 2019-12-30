from tor_server import *

def main():
    tor = TorServer(15007)
    tor.create_threads()
    tor.create_jobs() 

main()
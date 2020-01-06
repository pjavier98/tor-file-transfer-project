# tor-file-transfer-project
File transfer project using sockets, python and threads.

The project consists of an application where it has a central server and 
several clients that will connect to this server by setting up a network.

Users can do file searches on the server and do
upload and download these files.

Server: Tor-Server
Users: Client-Server (Peer-to-Peer / P2P)

## Application Installation and Execution:

* Must be with Python installed, preferably on latest version Updated 
(Version used: Python 3.6.8)

* You need to use the library (tqdm) to use the progressive bar:

#### TQDM Library Installation:
```
pip/pip3 install tqdm
```
or
```
conda install -c conda-forge tqdm
```
or
```
snap install tqdm
```

* Open your terminal and run the followings commands to run a client:
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project

cd tor-project

python3 main_client.py
```

* Now you are ready to download and upload files, share knowledge and other
things with other people around the world!

## Tor-Server:
Tor-Server was hosted at DigitalOcean.

To execute the server run the followings commands:
```
ssh root@(IP_FROM_SERVER)
```
Then enter your password and run
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project

cd tor-project

python3 main_server.py
```




# tor-file-transfer-project
File transfer project using sockets, python and threads.

The project consists of an application where it has a central server and 
several clients that will connect to this server by setting up a network.

Users can do file searches on the server and do upload and download these
files.

Server: Tor-Server.
Users: Client-Server (Peer-to-Peer / P2P).

## Application Installation and Execution:

* Must be with Python installed, preferably on latest version Updated 
(Version used: Python 3.6.8)

[Install Python for Linux/MacOS/Windows](https://www.python.org/downloads/)


* Must be with pip3 installed
 
[How to install pip3 on Linux](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)

[How to install pip3 on MacOS](https://evansdianga.com/install-pip-osx/)

[How to install pip3 on Windows](https://vgkits.org/blog/pip3-windows-howto/)

* You need to use the library (tqdm) to use the progressive bar:

[How to install tqdm](https://tqdm.github.io/)

Select one of the commands below:

Linux:
```
pip3 install tqdm
```
```
conda install -c conda-forge tqdm
```
```
snap install tqdm
```

MacOS:
```
pip3 packageName
```

Windows:
```
pip install packageName
```

## To execute the project locally:
### Tor-Server:
Open your terminal and run the followings commands to run the tor-server:
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project/tor-project

python3 main_server.py
```

### Tor-Client:
Open your terminal and run the followings commands to run a tor-client:
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project/tor-project

python3 main_client.py
```

## To execute the project using a hosted server:
### Tor-Server:
Tor-Server was hosted at DigitalOcean.

To execute the server run the followings commands:
```
ssh root@(IP_FROM_SERVER)
```
Then enter your password and run:
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project/tor-project

python3 main_server.py
```
### Tor-Client:
Open your terminal and run the followings commands to run a tor-client:
```
git clone https://github.com/pjavier98/tor-file-transfer-project

cd tor-file-transfer-project/tor-project

python3 main_client.py
```


Now you are ready to download and upload files, share knowledge and other
things with other people around the world!!!

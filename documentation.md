# tor-file-transfer-project
File transfer project using sockets, python and threads.

The project consists of an application where it has a central server and 
several clients that will connect to this server by setting up a network.

Users can do file searches on the server and do upload and download these
files.

Server: Tor-Server
Users: Client-Server (Peer-to-Peer / P2P)

## TFTCP (Tor-File-Transfer-Control-Protocol)
All commands that are entered by the user are sent to the server,
it performs a check if those commands are correct and returns
an answer to the actions being taken. That is, all verifications are
made on the server to prevent the user from manipulating the client file
and may damage the operation of the server.

Request-Response:
```
  If the command the client send is correct:
    'ok'
  Else:
    'This command does not exist, rewrite'
*-------------------------------------------------------------------------*
  If the client request to show or search something, to finalize the sent of the content:
    'end'
*-------------------------------------------------------------------------*
  If the client request to download or upload something, to confirm the file exist:
    'found'
  Else:
    'Not found file'
*-------------------------------------------------------------------------*
  If a user wants to sign out:
    'exit'
  Communicating to server to kill connection with him and he disconnects
*-------------------------------------------------------------------------*
  To finalize the sent of a file, initially the total size of the file is sent
```

## Tor-Server:

The server has a folder called "tor_files" where all the files are
files that the server has, (the ones it already had and the ones that
upload).

The server can also execute commands on it simultaneously with commands
submitted by clients such as:

```
>> list
List the connections and the amount of online clients
*-------------------------------------------------------------------------*
>> clear
Clean the terminal
*-------------------------------------------------------------------------*
>> exit
Logs out if no clients are online
```

## Clients:
When the application is started, the host and port of the server that requires
will connect, a folder named 'tor-files' is also created. Inside the
It will create two folders, 'Downloads' and 'Uploads'. In the folder
downloads were all files downloaded from the server and in the folder of
uploads should be placed the files that will be uploaded to the
server.

Commands that can be executed by the clients:
```
>> show
Lists all files the server has
*-------------------------------------------------------------------------*
>> search <filename>
List all files containing the specified substring (.pdf, .mp4)
*-------------------------------------------------------------------------*
>> upload <filename>
Upload a user field to the server
*-------------------------------------------------------------------------*
>> download <filename>
Download a file from the server
*-------------------------------------------------------------------------*
>> exit
Communicates to server that will disconnect and terminates its connection
```
# tor-file-transfer-project
Projeto de transferência de arquivos usando sockets, python e threads.

O projeto consiste em uma aplicação onde tem um servidor central e vários
clientes que vão se conectar a este servidor configurando uma rede.

Servidor: Tor-Server
Users: Client-Server (Porta) (Peer-to-Peer / P2P)

## Tor-Server:
Tem a responsabilidade de salvar as conexões ativas dos clientes.


## Users: Client-Server (P2P): 
Cada usuário ao iniciar sessão cria uma pasta com o nome da porta.

Ex: 
```
mkdir user_<numero_da_porta>

mkdir user_15000
```

Um usuário possui um cliente e servidor, possibilitando enviar e receber
arquivos sem ser necessário um servidor centralizado. O tor-server apenas
possui os nomes dos usuários ativos e quem está ativo.

![Client-Server](img/client-server.jpg)



## Protocolo de envio de arquivos (fluxo):
O fluxo de envio de arquivos será o seguinte:

1. O cliente de um usuário solicita que quer um arquivo x, o servidor pergunta
aos usuários ligados a ele se alguém possui aquele arquivo e está disposto
a compartilha-lo.

2. Se a resposta for que ninguém tem o arquivo o servidor responde ao
cliente que solicitou o arquivo que não foi possível encontrar tal arquivo
na rede.

3. Se alguém possui o arquivo, o servidor pergunta a quem solicitou se 
ele gostaria de fazer download de aquele arquivo, caso sim o servidor
envia para o possuidor do arquivo um array com os endereços de todos os
usuários conectados na rede e uma hash (por enquanto só a porta mesmo) 
do destinatário.

4. A cada pacote enviado é repetido o processo, o provedor vai consumindo a
lista a partir de um determinado ponto (pode ser aleatório) e vai
perguntando ao usuário se seu nome coincide com o do usuário final. Caso
coincidir o pacote é enviado.

5. A busca do usuário final vai ser um BFS.

![Graph](img/graph.jpg)
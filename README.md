# TCP Chat in Python

This project is a TCP chat application built with Python sockets.

I started this project to better understand how the following concepts work in practice:

- Client-server communication
- File transfer
- Multiple users handling
- TCP protocols
- Threads
- Connection management

The project is still under development, and I am currently redesigning parts of it to improve the architecture and fix issues I discovered during testing.

# Current Features
Message sending
File transfer
Header-based protocol to identify data type and size
TCP communication
One thread per client
# What I Have Learned So Far

During development, I started to better understand concepts such as:

- TCP does not separate messages automatically
- recv() may return fragmented data
- Messages and files require their own protocol structure
- Each client needs its own connection state
- recv() blocks while waiting for incoming data
- The difference between text and bytes in Python
# Current Protocol Structure

At the moment, messages use a simple header containing information such as:

- Content type
- Data size

This helps prevent issues where messages and files get mixed together during transmission.

# Technologies Used
- Python
- socket
- threading
# Future Goals
- Improve multi-client handling
- Add queue systems
- Improve protocol organization
- Learn asyncio
- Improve error handling
- Add logging system
# Motivation

I am mainly using this project to practice backend development, networking concepts, and communication logic between distributed systems.

-----------------------------------------------------------------------------------------------------------------------------------------
# Chat TCP em Python

Esse projeto é um chat feito com sockets TCP em Python.

Comecei ele para aprender melhor como funciona:
- comunicação entre cliente e servidor
- envio de arquivos
- múltiplos usuários
- protocolos TCP
- threads
- tratamento de conexões

O projeto ainda está em desenvolvimento e estou recriando partes dele para melhorar a arquitetura e corrigir problemas que fui entendendo durante os testes.

---

# Funcionalidades atuais

- Envio de mensagens
- Envio de arquivos
- Cabeçalho para identificar tipo e tamanho dos dados
- Comunicação TCP
- Thread por cliente

---

# O que aprendi até agora

Durante o desenvolvimento comecei a entender melhor coisas como:

- TCP não separa mensagens automaticamente
- recv() pode retornar dados fragmentados
- arquivos e mensagens precisam de protocolo próprio
- cada cliente precisa do seu próprio estado/conexão
- recv() fica bloqueado esperando dados
- diferença entre texto e bytes em Python

---

# Estrutura atual do protocolo

Atualmente as mensagens utilizam um cabeçalho simples contendo informações como:
- tipo do conteúdo
- tamanho dos dados

Isso ajuda a evitar problemas de mistura entre mensagens e arquivos.

---

# Tecnologias usadas

- Python
- socket
- threading

---

# Objetivos futuros

- Melhorar tratamento de múltiplos clientes
- Adicionar sistema de filas
- Melhorar organização do protocolo
- Aprender asyncio
- Melhorar tratamento de erros
- Adicionar logs

---

# Motivação

Estou usando esse projeto principalmente para praticar backend, redes e lógica de comunicação entre sistemas.

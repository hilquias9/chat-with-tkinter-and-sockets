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
- Tkinter
# Future Goals
- Improve multi-client handling
- Add queue systems
- Improve protocol organization
- Learn asyncio
- Improve error handling
- Add logging system
# Motivation

I am mainly using this project to practice backend development, networking concepts, and communication logic between distributed systems.

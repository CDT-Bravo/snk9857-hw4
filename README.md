# Basic C2

This basic C2 Implant is a command-and-control (C2) agent designed to provide remote execution capabilities on a compromised linux system. The script has mechanisms to establish persistence, periodically check for commands from the C2 server, executes them, and sends back the results. 
## Installation

Install server2.py on the server, or host, and install client.py on the target machine. Make sure to edit the client.py file with the IP address of your server.

## Usage
Both files need to be running for the C2 to work. 

Run server2.py on the server (host) machine. 
```python
chmod +x server2.py
./server2.py
```
Run client.py on the target machine using sudo and admin permissions in order to establish persistance.
```python
chmod +x client.py
sudo ./client.py
```

## Required
Ensure flask is installed on the server (host) in order for the script to run correctly.
```python
pip install flask
```

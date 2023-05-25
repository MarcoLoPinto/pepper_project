import eventlet
eventlet.monkey_patch()

import socket
import threading
from command import Command

class IPCServer():
    def __init__(self) -> None:
        self.send_command = None
        self.client_sockets = {}
        self.sockets_lock = threading.Lock()
        self.sock = None
    
    def run(self, port=5001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(1)
        self.sock.bind(("localhost",port))
        self.sock.listen(20)
        t = threading.Thread(target=self.wait_connection)
        t.start()
    
    def wait_connection(self):
        while True:
            if self.sock == None:
                break
            try:
                client_sock, addr = self.sock.accept()
                addr = f"{addr[0]}:{addr[1]}"
                self.sockets_lock.acquire()
                self.client_sockets[addr] = client_sock
                self.sockets_lock.release()
                t = threading.Thread(target=self.receive_command, args=[client_sock, addr])
                t.start()
                print(f"{addr} connected to IPC module")
            except Exception as e:
                continue

    def disconnect(self):
        print("Disconnetting ipc server...")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.sock = None
        self.sockets_lock.acquire()
        keys = list(self.client_sockets.keys())
        for addr in keys:
            sock = self.client_sockets.pop(addr)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        self.sockets_lock.release()
        print("Ipc server disconnected")
            
    def receive_command(self, client_sock: socket.socket, addr: str):
        """
        Loop that waits and accepts requests and responses from the python 2 client
        It takes every command sent by the robot scripts and forwards it to the browser
        """
        full_data = ""
        while True:
            data = client_sock.recv(1024)
            # self.disconnect() has been called, exit the loop and shutdown the thread
            if self.sock == None:
                break
            # the client disconnected, remove its socket from the dict and shutdown the thread
            if not data:
                print(f"{addr} disconnected from IPC module")
                self.sockets_lock.acquire()
                if addr in self.client_sockets:
                    self.client_sockets.pop(addr)
                self.sockets_lock.release()
                break
            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                full_data = full_data[:-2]
                command = Command.fromJson(full_data)
                full_data = ""
                if self.send_command != None:
                    self.send_command(command)

    def dispatch_command(self, command: Command):
        """
        Called when a command is received from the browser and needs to be forwarded to the python 2 robot client
        """
        for addr, sock in self.client_sockets.items():
            try:
                sock.sendall(command.toBytes()+b"\r\t")
            except Exception as e:
                print(f"Failed to dispatch command to {addr}")
                continue
    
    def set_command_listener(self, func):
        """
        Sets the function to be called when the client sends a command to this server
        """
        self.send_command = func
import socket
import threading
from command import Command

class IPCServer():
    def __init__(self) -> None:
        self.send_command = None
        self.client_sock = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t = None
    
    def run(self, port=5001):
        self.sock.bind(("localhost",port))
        self.sock.listen(1)
        self.client_sock, addr = self.sock.accept()
        self.t = threading.Thread(target=self.receive_command)
        self.t.start()

    def disconnect(self):
        print("Disconnetting ipc server...")
        self.sock.close()
        if self.t != None: self.t = None

    def receive_command(self):
        """
        Loop that waits and accepts requests and responses from the python 2 client
        It takes every command sent by the robot scripts and forwards it to the browser
        """
        full_data = ""
        while self.t != None:
            data = self.client_sock.recv(1024)
            if not data:
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
        if self.client_sock == None: return
        self.client_sock.sendall(command.toBytes()+b"\r\t")
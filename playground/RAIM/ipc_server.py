import socket
import threading
from command import Command

class IPCServer():
    def __init__(self) -> None:
        self.send_command = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self, port=5001):
        self.sock.bind(("localhost",port))
        self.sock.listen(1)
        self.client_sock, addr = self.sock.accept()
        t = threading.Thread(target=self.receive_command)
        t.start()

    def receive_command(self):
        """
        Loop that waits and accepts requests and responses from the python 2 client
        It takes every command sent by the robot scripts and forwards it to the browser
        """
        full_data = ""
        while True:
            data += self.client_sock.recv(1024)
            if not data:
                break
            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                command = Command.fromJson(data)
                data = ""
                if self.send_command != None:
                    self.send_command(command)

    def dispatch_command(self, command: Command):
        """
        Called when a command is received from the browser and needs to be forwarded to the python 2 robot client
        """
        self.client_sock.sendall(command.toBytes())
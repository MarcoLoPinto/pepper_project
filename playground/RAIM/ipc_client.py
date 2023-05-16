import socket
import threading
from command import Command

class IPCClient():
    def __init__(self) -> None:
        self.execute_command = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self, port=5001):
        self.sock.connect(("localhost",port))
        t = threading.Thread(target=self.receive_command)
        t.start()

    def receive_command(self):
        """
        Loop that waits and accepts requests and responses from the python 3 server
        It takes every command sent by the browser and executes it on the robot
        """
        full_data = ""
        while True:
            data += self.sock.recv(1024)
            if not data:
                break
            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                command = Command.fromJson(data)
                data = ""
                if self.execute_command != None:
                    self.execute_command(command)

    def dispatch_command(self, command: Command):
        """
        Called when a command or response from the robot needs to be forwarded to the browser 
        """
        self.sock.sendall(command.toBytes())
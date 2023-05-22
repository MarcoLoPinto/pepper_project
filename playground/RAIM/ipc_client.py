import socket
import threading
from command_py2 import Command

class IPCClient():
    def __init__(self):
        self.execute_command = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t = None
    
    def connect(self, port=5001):
        self.sock.connect(("localhost",port))
        self.t = threading.Thread(target=self.receive_command)
        self.t.start()
    
    def disconnect(self):
        print("Disconnecting ipc client...")
        self.sock.close()
        if self.t != None: self.t = None

    def receive_command(self):
        """
        Loop that waits and accepts requests and responses from the python 3 server
        It takes every command sent by the browser and executes it on the robot
        """
        full_data = ""
        while self.t != None:
            data = self.sock.recv(1024)
            if not data:
                break
            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                full_data = full_data[:-2]
                command = Command.fromJson(full_data)
                full_data = ""
                if self.execute_command != None:
                    self.execute_command(command)

    def dispatch_command(self, command):
        """
        Called when a command or response from the robot needs to be forwarded to the browser 
        """
        self.sock.sendall(command.toBytes())
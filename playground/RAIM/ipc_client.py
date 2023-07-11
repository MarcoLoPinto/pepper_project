import socket
import threading
import random
from .ipc_command import Command

class IPCClient():
    def __init__(self, name="IPCClient_"+str(random.randint(1000,9999))):
        self.name = name # The name of this client. Command having id equal to this name will be sent to this client
        self.execute_command = None # The function called when the server sends a command to this client 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t = None
    
    def connect(self, host="localhost", port=5001):
        """
        Connects this client to the server using the provided port
        """
        self.sock.connect((host,port))
        self.sock.sendall(self.name.encode("utf-8")) 
        self.t = threading.Thread(target=self.receive_command)
        self.t.start()
    
    def disconnect(self):
        """
        Disconnects this client from the server
        """
        print("Disconnecting ipc client...")
        self.sock.shutdown(socket.SHUT_RDWR)
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
                    print("IPCClient receive_command")
                    self.execute_command(command)

    def dispatch_command(self, command):
        """
        Called when this client has to send a command to another client/browser.
        The command.to_client_id decides the receiver. If command.to_client_id is 0 the command is broadcasted
        """
        if command.from_client_id == "": command.from_client_id = self.name
        self.sock.sendall(command.toBytes()+b"\r\t")
    
    def set_command_listener(self, func):
        """
        Sets the function to be called (callback) when the server has a command for this client
        """
        self.execute_command = func
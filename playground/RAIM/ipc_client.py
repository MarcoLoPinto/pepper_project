import socket
import threading
import random
from .raim_command import Command

class IPCClient():
    def __init__(self, name="IPCClient_"+str(random.randint(1000,9999))):
        self.name = name # The name of this client. Command having id equal to this name will be sent to this client
        self.general_command_listener = None # The function called when the server sends a command to this client
        self.on_connect = None # Callback called when the connection opens
        self.on_disconnect = None # Callback called when the connection closes
        self.response_callbacks = {} # A disctionary of command id to callbacks
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t = None
    
    def connect(self, host="localhost", port=5001):
        """
        Connects this client to the server using the provided port
        """
        self.sock.connect((host,port))
        self.sock.sendall(self.name.encode("utf-8"))
        if self.on_connect != None: self.on_connect()
        self.t = threading.Thread(target=self.receive_command)
        self.t.start()
    
    def disconnect(self):
        """
        Disconnects this client from the server
        """
        print("Disconnecting IPC client %s..." %(self.name))
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        if self.t != None: self.t = None
        if self.on_disconnect != None: self.on_disconnect()

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
                print("%s received a command from %s: %s" %(self.name, command.from_client_id, command.data))
                self.__internal_dispatch_command(command)
    
    def __internal_dispatch_command(self, command):
        """
        Internal function to check wheter this command is a response or is request/standalone command from another client
        """
        if command.request == False and command.id in self.response_callbacks:
            response_callback = self.response_callbacks.pop(command.id)
            response_callback(command)
        elif self.general_command_listener != None:
            self.general_command_listener(command)

    def dispatch_command(self, command, response_callback = None):
        """
        Called when this client has to send a command to another client.
        The command.to_client_id decides the receiver. If command.to_client_id is 0 the command is broadcasted
        """
        if command.from_client_id == "": command.from_client_id = self.name
        if response_callback != None and command.request == True:
            self.response_callbacks[command.id] = response_callback
        self.sock.sendall(command.toBytes()+b"\r\t")
    
    def set_command_listener(self, func):
        """
        Sets the function to be called (callback) when the server has a command for this client that is not a response to another request
        """
        self.general_command_listener = func
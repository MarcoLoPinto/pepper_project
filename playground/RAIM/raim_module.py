import socket
import threading
from .raim_command import Command

class RAIMModule():
    def __init__(self) -> None:
        self.module_name = "Module"
        self.dispatch_command_to_module_functions = []
        self.client_sockets = {}
        self.sockets_lock = threading.Lock()
        self.sock = None
    
    def run(self, port=5001):
        pass
    
    def disconnect(self):
        pass
    
    def wait_for_connection(self):
        pass
            
    def receive_command(self, client_sock: socket.socket):
        """
        Loop that waits and accepts requests and responses from the clients
        """
        pass

    def dispatch_command(self, command: Command, primary_dispatch: bool = False) -> bool:
        """
        Called when a command is received from a client and has to be forwarded to the other clients
        If this is a primary dispatch, all the attached modules should be called
        Return whether the dispatch has been executed by this or any other modules
        """
        pass

    
    def add_dispatch_to_module_fn(self, func):
        """
        Add a module dispatch_command function 
        """
        self.dispatch_command_to_module_functions.append(func)
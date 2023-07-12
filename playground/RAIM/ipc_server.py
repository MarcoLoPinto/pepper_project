# import eventlet
# eventlet.monkey_patch()

import socket
import threading
from .raim_command import Command

class IPCServer():
    def __init__(self) -> None:
        self.module_name = "IPC"
        self.dispatch_command_to_module_functions = []
        self.client_sockets = {}
        self.sockets_lock = threading.Lock()
        self.sock = None
    
    def run(self, port=5001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(1)
        self.sock.bind(("0.0.0.0",port))
        self.sock.listen(1000)
        t = threading.Thread(target=self.wait_for_connection)
        t.start()
    
    def disconnect(self):
        print("Disconnetting IPC server...")
        with self.sockets_lock:
            keys = list(self.client_sockets.keys())
            for addr in keys:
                sock = self.client_sockets.pop(addr)
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        self.sock = None
        print("IPC server disconnected")
    
    def wait_for_connection(self):
        while True:
            if self.sock == None:
                break
            try:
                client_sock, addr = self.sock.accept()
                # addr = f"{addr[0]}:{addr[1]}"
                client_name = client_sock.recv(1024).decode("utf-8")
                if not client_name:
                    continue
                with self.sockets_lock:
                    self.client_sockets[client_name] = client_sock
                t = threading.Thread(target=self.receive_command, args=[client_sock, client_name])
                t.start()
                print(f"{client_name} connected to IPC module")
            except Exception as e:
                continue
            
    def receive_command(self, client_sock: socket.socket, client_name: str):
        """
        Loop that waits and accepts requests and responses from the ipc clients
        """
        full_data = ""
        while True:
            data = client_sock.recv(1024)
            # self.disconnect() has been called, exit the loop and shutdown the thread
            if self.sock == None:
                break
            # the client disconnected, remove its socket from the dict and shutdown the thread
            if not data:
                print(f"{client_name} disconnected from IPC module")
                with self.sockets_lock:
                    if client_name in self.client_sockets:
                        self.client_sockets.pop(client_name)
                break

            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                full_data = full_data[:-2]
                command = Command.fromJson(full_data)
                full_data = ""
                self.dispatch_command(command, primary_dispatch=True)

    def dispatch_command(self, command: Command, primary_dispatch: bool = False) -> bool:
        """
        Called when a command is received from a client and has to be forwarded to the other clients
        If this is a primary dispatch, all the attached modules should be called
        Return whether the dispatch has been executed by this or any other modules
        """
        if primary_dispatch: print(f"Command received by IPC module, from {command.from_client_id}, to {command.to_client_id}: {command.data}")

        # When the client_id is 0, the command is broadcasted
        if command.to_client_id == "0":
            # First dispatching to all the connected websocket
            for client_name, sock in self.client_sockets.items():
                if client_name == command.from_client_id: continue
                try:
                    sock.sendall(command.toBytes()+b"\r\t")
                except Exception as e:
                    print(f"Failed to dispatch command to {client_name}")
                    continue
            # Then dispatching to all the other connected modules, but only if this is the primary dispatch command
            if primary_dispatch:
                for dispatch_fn in self.dispatch_command_to_module_functions:
                    dispatch_fn(command, primary_dispatch = False)
            
            return True

        # client_id is single client
        else:
            client_name = command.to_client_id
            # First check if the client is connected to this module
            if client_name in self.client_sockets:
                sock = self.client_sockets[client_name]
                try:
                    sock.sendall(command.toBytes()+b"\r\t")
                    return True
                except Exception as e:
                    print(f"Failed to dispatch command to {command.to_client_id}")
                    return False
            # Then try dispatching to all the other connected modules, but only if this is the primary dispatch command
            if primary_dispatch:
                for dispatch_fn in self.dispatch_command_to_module_functions:
                    dispatch_result = dispatch_fn(command, primary_dispatch=False)
                    if dispatch_result == True: 
                        return True
            
            return False

    
    def add_dispatch_to_module_fn(self, func):
        """
        Add a module dispatch_command function 
        """
        self.dispatch_command_to_module_functions.append(func)
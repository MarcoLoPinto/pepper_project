import websockets
import threading
from raim_command import Command
from websockets.sync.server import serve

class WebsocketServer():
    def __init__(self) -> None:
        self.module_name = "Websocket"
        self.dispatch_command_to_module_functions = []
        self.client_sockets = {}
        self.sockets_lock = threading.Lock()
        self.server = None
    
    def run(self, port=5002):
        t = threading.Thread(target=self.wait_for_connection, args=[port])
        t.start()
    
    def disconnect(self):
        print("Disconnetting Websocket module...")
        with self.sockets_lock:
            keys = list(self.client_sockets.keys())
            for client_name in keys:
                sock = self.client_sockets.pop(client_name)
                sock.close()
        self.server.shutdown()
        self.server = None
        print("Websocket server disconnected")
    
    def wait_for_connection(self, port):
        with websockets.sync.server.serve(self.receive_command,host="0.0.0.0", port=port) as server:
            self.server = server
            server.serve_forever()
            
    def receive_command(self, client_sock: websockets.sync.server.ServerConnection):
        """
        Loop that waits and accepts requests and responses from a websocket client
        """
        try:
            client_name = client_sock.recv()
            print(f"{client_name} connected to Websocket module")
        except:
            return

        with self.sockets_lock:
            self.client_sockets[client_name] = client_sock

        try:
            while True:
                data = client_sock.recv()
                command = Command.fromJson(data)
                print(f"Command ({command.id} | request:{command.request}) received by Websocket module, from {command.from_client_id}, to {command.to_client_id}: {command.data}")
                self.dispatch_command(command, primary_dispatch = True)
        except:
            print(f"{client_name} disconnected from Websocket module")
            with self.sockets_lock:
                if client_name in self.client_sockets:
                    self.client_sockets.pop(client_name)

    def dispatch_command(self, command: Command, primary_dispatch: bool = False) -> bool:
        """
        Called when a command is received from a client and has to be forwarded to the other clients
        If this is a primary dispatch, all the attached modules should be called
        Return whether the dispatch has been executed by this or any other modules
        """

        # When the client_id is 0, the command is broadcasted
        if command.to_client_id == "0":
            # First dispatching to all the connected websocket
            for client_name, sock in self.client_sockets.items():
                if client_name == command.from_client_id: continue
                try:
                    sock.send(command.toJson())
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
                    sock.send(command.toJson())
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
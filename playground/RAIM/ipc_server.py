import eventlet
eventlet.monkey_patch()

import socket
import threading
from command import Command

class IPCServer():
    def __init__(self) -> None:
        self.send_command_to_browser = None
        self.client_sockets = {}
        self.sockets_lock = threading.Lock()
        self.sock = None
    
    def run(self, port=5001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(1)
        self.sock.bind(("0.0.0.0",port))
        self.sock.listen(20)
        t = threading.Thread(target=self.wait_ipc_connection)
        t.start()
    
    def wait_ipc_connection(self):
        while True:
            if self.sock == None:
                break
            try:
                client_sock, addr = self.sock.accept()
                # addr = f"{addr[0]}:{addr[1]}"
                client_name = client_sock.recv(1024).decode("utf-8")
                if not client_name:
                    continue
                self.sockets_lock.acquire()
                self.client_sockets[client_name] = client_sock
                self.sockets_lock.release()
                t = threading.Thread(target=self.receive_command, args=[client_sock, client_name])
                t.start()
                print(f"{client_name} connected to IPC module")
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
            
    def receive_command(self, client_sock: socket.socket, client_name: str):
        """
        Loop that waits and accepts requests and responses from the python 2 ipc clients
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
                print(f"{client_name} disconnected from IPC module")
                self.sockets_lock.acquire()
                if client_name in self.client_sockets:
                    self.client_sockets.pop(client_name)
                self.sockets_lock.release()
                break

            full_data += data.decode("utf-8")
            if full_data.endswith("\r\t"):
                full_data = full_data[:-2]
                command = Command.fromJson(full_data)
                full_data = ""
                self.dispatch_command(command)

    def dispatch_command(self, command: Command):
        """
        Called when a command is received from a client and has to be forwarded to the other clients
        """
        print(f"Command received, from {command.from_client_id}, to {command.to_client_id}: {command.data}")

        # When the client_id is 0, the command is broadcasted
        if command.to_client_id == "0":
            if self.send_command_to_browser != None and command.from_client_id != "browser":
                self.send_command_to_browser(command)
            for client_name, sock in self.client_sockets.items():
                if client_name == command.from_client_id: continue
                try:
                    sock.sendall(command.toBytes()+b"\r\t")
                except Exception as e:
                    print(f"Failed to dispatch command to {client_name}")
                    continue
        
        # When the client_id is browser, the command is sent via socketio
        elif command.to_client_id == "browser":
            if self.send_command_to_browser != None:
                self.send_command_to_browser(command)
                return

        # client_id is an ipc client
        else:
            client_name = command.to_client_id
            if client_name in self.client_sockets:
                sock = self.client_sockets[client_name]
                try:
                    sock.sendall(command.toBytes()+b"\r\t")
                except Exception as e:
                    print(f"Failed to dispatch command to {command.to_client_id}")
                finally:
                    return

    
    def set_fn_send_command_to_browser(self, func):
        """
        Sets the function to be called when a client sends a command to the browser
        """
        self.send_command_to_browser = func
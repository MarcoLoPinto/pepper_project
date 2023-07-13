#!/usr/bin/env python3
import os
import sys
import signal
from flask import Flask, send_file
from ipc_server import IPCServer
from websocket_server import WebsocketServer
from raim_command import Command

DIR = os.path.realpath(os.path.dirname(__file__))

# Rich Advanced Interaction Manager
class RAIMServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.modules = [IPCServer(),WebsocketServer()]

        for i in range(len(self.modules)):
            current_module = self.modules[i]
            rest_of_modules = [mod for j, mod in enumerate(self.modules) if j != i]
            for mod in rest_of_modules:
                current_module.add_dispatch_to_module_fn(mod.dispatch_command)
        
        @self.app.route("/")
        def index():
            return send_file(f"{DIR}/pages/index.html")
        @self.app.route("/<path:filename>")
        def serve(filename):
            path = f"{DIR}/pages/{filename}"
            # return send_file(path)
            if os.path.exists(path):
                return send_file(path)
            else:
                return "Error 404, Not Found", 404

    def run(self,port=5000):
        for i, mod in enumerate(self.modules):
            print(f"Running {mod.module_name} module on port {port+i+1} ...")
            mod.run(port+i+1)

        print(f"Running http server on 0.0.0.0:{port} ...")
        self.app.run(port=port)
    
    def disconnect_modules(self):
        for mod in self.modules:
            mod.disconnect()

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    try:
        app = RAIMServer()
        app.run(port=port)
    except KeyboardInterrupt:
        app.disconnect_modules()
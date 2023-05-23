#!/usr/bin/env python3
import os
import sys
import signal
from flask import Flask, send_file
from flask_socketio import SocketIO
from ipc_server import IPCServer
from command import Command

DIR = os.path.realpath(os.path.dirname(__file__))

# Rich Advanced Interaction Manager
class RAIMServer:
    def __init__(self):
        template_dir = os.path.abspath('pages')
        self.app = Flask(__name__, template_folder=template_dir)
        self.socketio = SocketIO(self.app)
        self.ipc = IPCServer()
        
        @self.app.route("/")
        def index():
            return send_file(f"{DIR}/pages/index.html")
        @self.app.route("/<filename>")
        def serve(filename):
            path = f"{DIR}/pages/{filename}"
            # return send_file(path)
            if os.path.exists(path):
                return send_file(path)
            else:
                return "Error 404, Not Found", 404
        
        @self.socketio.on('command')
        def browser_command(command_json: str):
            command = Command.fromJson(command_json)
            print(f"Command {command.id} received: {command.data}")
            self.ipc.dispatch_command(command)

        # executed when a client sends a request
        self.ipc.send_command = lambda c: self.robot_command(c) 

    def robot_command(self, command: Command):
        self.socketio.emit("command",command.toJson())

    def run(self,port=5000):
        print("Running ipc server...")
        self.ipc.run(port+1)
        print("Running http server...")
        self.socketio.run(self.app, port=port)

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    try:
        app = RAIMServer()
        app.run(port=port)
    except KeyboardInterrupt:
        app.ipc.disconnect()
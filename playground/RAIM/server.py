#!/usr/bin/env python3
from flask import Flask, render_template
from flask_socketio import SocketIO
from ipc_server import IPCServer
from command import Command

# Rich Advanced Interaction Manager
class RAIMServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(app)
        self.ipc = IPCServer()
        
        @self.app.route("/")
        def index():
            return render_template('index.html')
        
        @self.socketio.on('command')
        def browser_command(command: Command):
            self.ipc.dispatch_command(command)

        self.ipc.send_command = lambda c: self.robot_command(c) 

    def robot_command(self, command: Command):
        self.socketio.emit("command",command.toJson())

    def run(self,port=5000):
        self.ipc.run(port+1)
        self.socketio.run(app, port=port)

if __name__ == "__main__":
    app = RAIMServer()
    app.run()
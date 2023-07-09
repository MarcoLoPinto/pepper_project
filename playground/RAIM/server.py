import os
import sys
import signal
from flask import Flask, send_file
from ipc_server import IPCServer
from command import Command

import asyncio
from websocket_server import WebsocketServer

import threading

DIR = os.path.realpath(os.path.dirname(__file__))
CERT_PATH = f"{DIR}/certs/cert.pem"
KEY_PATH = f"{DIR}/certs/key.pem"

class RAIMServer():
    def __init__(self):
        self.app = Flask(__name__)
        self.ipc = IPCServer()
        self.ws_server = None

        @self.app.route("/")
        def index():
            return send_file(f"{DIR}/pages/index.html")
        @self.app.route("/<path:filename>")
        def serve(filename):
            path = f"{DIR}/pages/{filename}"
            if os.path.exists(path):
                return send_file(path)
            else:
                return "Error 404, Not Found", 404
            
        # executed when a client sends a request
        self.ipc.set_fn_send_command_to_browser(lambda c: self.send_command_to_browser(c))
            
    def command_from_browser(self, client, server, command_json):
        command = Command.fromJson(command_json)
        self.ipc.dispatch_command(command)
            
        
    def send_command_to_browser(self, command: Command):
        self.ws_server.send_message_to_all(command.toJson())

    def run(self, port=5000):
        print(f"Running ipc server on port {port+1}...")
        self.ipc.run(port+1)
        print(f"Running websocket server on port {port+2}...")
        self.ws_server = WebsocketServer(host="0.0.0.0", port = port+2)
        self.ws_server.set_fn_message_received(self.command_from_browser)
        self.ws_server.run_forever(threaded=True)
        print(f"Running http server on port {port}...")
        self.app.run(ssl_context=(CERT_PATH,KEY_PATH))

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    try:
        app = RAIMServer()
        app.run(port=port)
    except KeyboardInterrupt:
        app.ipc.disconnect()
        app.ws_server.shutdown_abruptly()
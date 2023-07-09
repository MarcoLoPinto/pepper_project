import os
import sys
import signal
from flask import Flask, send_file
from ipc_server import IPCServer
from command import Command

import asyncio
import websockets

import threading

DIR = os.path.realpath(os.path.dirname(__file__))

class RAIMServer():
    def __init__(self):
        self.app = Flask(__name__)
        self.ipc = IPCServer()
        self.websockets = set()

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
            
    async def command_from_browser(self, websocket):
        print(websocket)
        self.websockets.add(websocket)
        while True:
            try:
                command_json = await websocket.recv()
                command = Command.fromJson(command_json)
                self.ipc.dispatch_command(command)
            except websockets.ConnectionClosedOK:
                self.websockets.remove(websocket)
                break
            
        
    def send_command_to_browser(self, command: Command):
        websockets.broadcast(self.websockets, command.toJson())

    async def _run_ws_serve(self, port):
        async with websockets.serve(self.command_from_browser, "localhost", port):
            await asyncio.Future()  # Run forever
    
    def _run_ws(self, port):
        asyncio.run(self._run_ws_serve(port=port))

    def run(self, port=5000):
        print(f"Running ipc server on port {port+1}...")
        self.ipc.run(port+1)
        print(f"Running websocket server on port {port+2}...")
        server_thread = threading.Thread(
            target=self._run_ws,
            args=(port+2,)
        )
        server_thread.start()
        print(f"Running http server on port {port}...")
        self.app.run(ssl_context='adhoc')

if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    try:
        app = RAIMServer()
        app.run(port=port)
    except KeyboardInterrupt:
        app.ipc.disconnect()
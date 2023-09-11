import os, sys
import signal
from pepperbot.PepperBot import PepperBot
import pepperbot.PepperMotions as motions
from RAIM.ipc_client import IPCClient
from RAIM.raim_command import Command

pepper_port = 34097
server_port = 5001
server_host = "localhost"
if len(sys.argv) > 1:
    pepper_port = int(sys.argv[1])
if len(sys.argv) > 2:
    server_port = int(sys.argv[2])

robot = PepperBot("127.0.0.1",pepper_port,alive=False)
ipc = IPCClient("talking_robot")

def shutdown(*args):
    print("Shutting down the script...")
    robot.quit()
    ipc.disconnect()

def speak(command):
    msg = command.data["msg"]
    print(msg)
    msg = msg.encode("ascii","replace")
    robot.say(msg, speed=60)
    if msg == "BYE":
        command = Command(data={"response": "The talking robot won't talk anymore..."}, to_client_id=command.from_client_id, request=False, id=command.id)
        ipc.dispatch_command(command)
        shutdown()
    if msg == "BACK2":
        command = Command(data={"response": "Response test"}, to_client_id=command.from_client_id, request=False, id=command.id)
        ipc.dispatch_command(command)
    if msg == "BACK":
        command = Command(data={"msg": "Full duplex test"}, to_client_id=command.from_client_id)
        ipc.dispatch_command(command)

ipc.set_command_listener(speak)

signal.signal(signal.SIGINT, shutdown) # Doesn't work. Stupid python 2!

ipc.connect(server_host, server_port)
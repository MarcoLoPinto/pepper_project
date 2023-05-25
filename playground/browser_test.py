import os, sys
import signal
from pepperbot.PepperBot import PepperBot
import pepperbot.PepperMotions as motions
from RAIM.ipc_client import IPCClient
from RAIM.command_py2 import Command

robot = PepperBot("127.0.0.1",33823,alive=False)
ipc = IPCClient()

def shutdown(*args):
    print("Shutting down the script...")
    robot.quit()
    ipc.disconnect()

def speak(command):
    msg = command.data["msg"]
    print(msg)
    msg = msg.encode("ascii","replace")
    robot.say(msg, speed=240)
    if msg == "BYE":
        shutdown()
    if msg == "TOUCH":
        command = Command(data={"data": "full duplex test"})
        ipc.dispatch_command(command)

ipc.set_command_listener(speak)

signal.signal(signal.SIGINT, shutdown) # Doesn't work. Stupid python 2!

ipc.connect()

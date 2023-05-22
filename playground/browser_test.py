import os, sys
from pepperbot.PepperBot import PepperBot
import pepperbot.PepperMotions as motions
from RAIM.ipc_client import IPCClient

try:
    robot = PepperBot("127.0.0.1",45653,alive=False)
    ipc = IPCClient()

    def speak(command):
        msg = command.data["msg"]
        print(msg)
        msg = msg.encode("ascii","replace")
        robot.say(msg, speed=120)
        if msg == "BYE":
            robot.quit()
            ipc.disconnect()
    ipc.execute_command = speak

    # def tst(command):
    #     msg = command.data["msg"]
    #     print msg
    # ipc.execute_command = tst

    ipc.connect()
except KeyboardInterrupt:
    ipc.disconnect()

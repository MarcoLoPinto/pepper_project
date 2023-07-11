# This file can be used to generate commands to test other connections
import os, sys
from RAIM.ipc_client import IPCClient
from RAIM.ipc_command import Command

ipc_server_host = "localhost"
ipc_server_port = 5001

ipc_tester = IPCClient("ipc_tester")
dispatch_and_disconnect = False # if false, wait for reply before disconnecting

# Create here a custom command

command_out_pepper_1 = Command(
    data={
        "actions": [
            {
                "action_type":"say_move",
                "action_properties": {
                    "text": "Hi, this is a long text to check if works!",
                    "move_name": "fancyRightArmCircle"
                },
            },
            {
                "action_type":"stand"
            }
            
        ]
        
    }, 
    to_client_id="pepper"
)

command_out_pepper_2 = Command(
    data={
        "actions": [
            {
                "action_type":"start_video"
            },
            {
                "action_type":"say",
                "action_properties": {
                    "text": "Hi, I'm starting the video!"
                },
            },
            {
                "action_type":"take_video_frame"
            }
            
        ]
        
    }, 
    to_client_id="pepper"
)

command_out_pepper_3 = Command(
    data={
        "actions": [
            {
                "action_type":"echo",
                "action_properties": {
                    "text": "Hi, I'm echoing!"
                },
            }
        ]
        
    }, 
    to_client_id="pepper"
)

command_out_pepper_4 = Command(
    data={
        "actions": [
            {
                "action_type":"quit",
            }
        ]
        
    }, 
    to_client_id="pepper"
)


# End creation

def echo_listener(command):
    print(command)
    ipc_tester.disconnect()

ipc_tester.set_command_listener(echo_listener)
ipc_tester.connect(host=ipc_server_host, port=ipc_server_port)
ipc_tester.dispatch_command(command_out_pepper_3) # set here the command to dispatch
if dispatch_and_disconnect:
    ipc_tester.disconnect()
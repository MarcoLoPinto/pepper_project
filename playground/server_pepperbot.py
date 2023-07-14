import os, sys
from RAIM.ipc_client import IPCClient
from RAIM.raim_command import Command

from pepperbot.PepperBot import PepperBot
import pepperbot.PepperMotions as motions

import argparse

class PepperServer:
    def __init__(self, ipc_server_host, ipc_server_port, pepper_host = "127.0.0.1", pepper_port = 9559, pepper_alive = False, **kwargs):
        self.pepper = PepperBot(pepper_host, pepper_port, alive=pepper_alive)
        self.ipc = IPCClient("pepper")
        
        self.ipc.set_command_listener(self.pepper_listener)
        self.ipc.connect(host=ipc_server_host, port=ipc_server_port)

    def shutdown(self):
        print("Shutting down the server...")
        self.ipc.disconnect()

    def pepper_listener(self, command):
        if "actions" in command.data:
            for action in command.data["actions"]:
                self.pepper_perform_action(command, action)

    def pepper_perform_action(self, command_in, action):
        # type: (Command, any) -> None
        action_type = action["action_type"]
        action_properties = None if "action_properties" not in action else action["action_properties"]
        # print("pepper received action:", action_type)
        # print("pepper received properties:", action_properties)

        if action_type == "say":
            self.pepper.say(action_properties["text"].encode('utf-8'))

        elif action_type == "stand":
            self.pepper.stand()

        elif action_type == "move":
            self.pepper.angleInterpolation(*getattr(motions, action_properties["move_name"].encode('utf-8'))())

        elif action_type == "say_move":
            ttt = self.pepper.say(action_properties["text"].encode('utf-8'), blocking=False)
            self.pepper.angleInterpolation(*getattr(motions, action_properties["move_name"].encode('utf-8'))())

        elif action_type == "quit":
            self.shutdown()

        elif action_type == "start_video":
            job_result = self.pepper.startVideoFrameGrabberEvent()
            if command_in.request:
                command_out = command_in.gen_response(is_successful = job_result)
            else:
                command_out = Command(
                    data={"action_type": action_type, "is_successful": job_result},
                    to_client_id=command_in.from_client_id
                )
            self.ipc.dispatch_command(command_out)

        elif action_type == "take_video_frame":
            frame_img = self.pepper.getCameraImageBase64()
            if command_in.request:
                command_out = command_in.gen_response(
                    data={"img": frame_img},
                    is_successful=frame_img is not None,
                )
            else:
                command_out = Command(
                    data={"img": frame_img, "is_successful": frame_img is not None},
                    to_client_id=command_in.from_client_id
                )
            self.ipc.dispatch_command(command_out)

        elif action_type == "echo": # only to debug if response is taken from server
            txt = action_properties["text"].encode('utf-8')
            self.pepper.say(txt)
            command_out = Command(
                data={"action_type_callback": action_type, "action_properties": {"echo": txt}},
                to_client_id=command_in.from_client_id
            )
            self.ipc.dispatch_command(command_out)
            
        elif action_type == "take_fake_video_frame": # only to debug
            frame_img = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAACxklEQVR4nOzTMREAIRDAwJ8fdGAeF6hDxhXZVZAm69z9QdU/HQCTDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmAtBcAAP//7QADfl8RE9gAAAAASUVORK5CYII="
            if command_in.request:
                command_out = command_in.gen_response(
                    data={"img": frame_img},
                    is_successful=frame_img is not None,
                )
            else:
                command_out = Command(
                    data={"img": frame_img, "is_successful": frame_img is not None},
                    to_client_id=command_in.from_client_id
                )
            self.ipc.dispatch_command(command_out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Recognition server')
    parser.add_argument('--ipc_server_host', type=str, default='localhost', help='IPC server hostname (default: localhost)')
    parser.add_argument('--ipc_server_port', type=int, default=5001, help='IPC server port number (default: 5001)')
    parser.add_argument('--pepper_host', type=str, default='127.0.0.1', help='Pepper robot hostname (default: 127.0.0.1)')
    parser.add_argument('--pepper_port', type=int, default=9559, help='Pepper robot port number (default: 9559)')
    parser.add_argument('--pepper_alive', type=bool, default=False, help='Pepper robot alive capability (default: False)')
    args = vars(parser.parse_args())

    pepper_server = PepperServer(**args)
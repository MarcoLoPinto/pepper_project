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

    def send_response(self, command_in, action_type, is_successful, action_properties = {}):
        # type: (Command, str, bool, dict) -> None
        data = {"action_type":action_type, "action_properties":action_properties, "is_successful":is_successful}
        if command_in.request:
            command_out = command_in.gen_response(is_successful = is_successful, data=data)
        else:
            command_out = Command(
                data=data,
                to_client_id=command_in.from_client_id
            )
        self.ipc.dispatch_command(command_out)

    def pepper_perform_action(self, command_in, action):
        # type: (Command, dict) -> None
        action_type = action["action_type"]
        action_properties = None if "action_properties" not in action else action["action_properties"]

        if action_type == "say":
            job_result = self.pepper.say(
                action_properties["text"].encode('utf-8'),
                blocking = command_in.request
            )
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {}
            )

        elif action_type == "stand":
            job_result = self.pepper.stand(blocking = command_in.request)
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {}
            )

        elif action_type == "move":
            job_result = self.pepper.angleInterpolation(
                *getattr(motions, action_properties["move_name"].encode('utf-8'))(),
                blocking = command_in.request
            )
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {}
            )

        elif action_type == "say_move":
            job_result_1 = self.pepper.say(action_properties["text"].encode('utf-8'), blocking=False)
            job_result_2 = self.pepper.angleInterpolation(
                *getattr(motions, action_properties["move_name"].encode('utf-8'))(),
                blocking = command_in.request
            )
            is_successful = job_result_1 is not False and job_result_2 is not False
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = is_successful,
                action_properties = {}
            )
        
        elif action_type == "say_move_led":
            job_result_1 = self.pepper.say(action_properties["text"].encode('utf-8'), blocking=False)
            job_result_2 = self.pepper.angleInterpolation(
                *getattr(motions, action_properties["move_name"].encode('utf-8'))(),
                blocking = False
            )
            job_result_3 = self.pepper.eyesColors(
                0 if "r" not in action_properties["r"].encode('utf-8') else int(action_properties["r"].encode('utf-8')),
                0 if "g" not in action_properties["g"].encode('utf-8') else int(action_properties["g"].encode('utf-8')),
                0 if "b" not in action_properties["b"].encode('utf-8') else int(action_properties["b"].encode('utf-8')),
                -1 if "duration" not in action_properties["duration"].encode('utf-8') else int(action_properties["duration"].encode('utf-8')),
                "Both" if "part" in action_properties["part"].encode('utf-8') else action_properties["part"].encode('utf-8')
            )
            is_successful = job_result_1 is not False and job_result_2 is not False and job_result_3 is not False
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = is_successful,
                action_properties = {}
            )

        elif action_type == "quit":
            self.shutdown()

        elif action_type == "start_video":
            job_result = self.pepper.startVideoFrameGrabberEvent()
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {}
            )

        elif action_type == "take_video_frame":
            frame_img = self.pepper.getCameraImageBase64()
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = frame_img is not None,
                action_properties = {"img": frame_img}
            )

        elif action_type == "set_volume":
            job_result = self.pepper.setVolume(
                float(action_properties["value"].encode('utf-8'))
            )
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {}
            )

        elif action_type == "echo": # only to debug if response is taken from server
            txt = action_properties["text"].encode('utf-8')
            job_result = self.pepper.say(txt, blocking = command_in.request)
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = job_result is not False,
                action_properties = {"echo": txt}
            )
            
        elif action_type == "take_fake_video_frame": # only to debug
            frame_img = "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAACxklEQVR4nOzTMREAIRDAwJ8fdGAeF6hDxhXZVZAm69z9QdU/HQCTDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmANAOQZgDSDECaAUgzAGkGIM0ApBmAtBcAAP//7QADfl8RE9gAAAAASUVORK5CYII="
            self.send_response(
                command_in = command_in, 
                action_type = action_type, 
                is_successful = frame_img is not None,
                action_properties = {"img": frame_img}
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Recognition server')
    parser.add_argument('--ipc_server_host', type=str, default='localhost', help='IPC server hostname (default: localhost)')
    parser.add_argument('--ipc_server_port', type=int, default=5001, help='IPC server port number (default: 5001)')
    parser.add_argument('--pepper_host', type=str, default='127.0.0.1', help='Pepper robot hostname (default: 127.0.0.1)')
    parser.add_argument('--pepper_port', type=int, default=9559, help='Pepper robot port number (default: 9559)')
    parser.add_argument('--pepper_alive', type=bool, default=False, help='Pepper robot alive capability (default: False)')
    args = vars(parser.parse_args())

    pepper_server = PepperServer(**args)
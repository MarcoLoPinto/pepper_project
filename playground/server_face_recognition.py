import os, sys
from FaceRecognition.fr_system import FaceRecognition
from RAIM.ipc_client import IPCClient
from RAIM.raim_command import Command

import argparse

class FaceRecognitionServer:
    def __init__(self, ipc_server_host, ipc_server_port, resize_value = 4, unknown_face_threshold = 10, debug = False, **kwargs) -> None:
        self.face_recognition = FaceRecognition(RESIZE_VALUE=resize_value, UNKNOWN_FACE_THRESHOLD=unknown_face_threshold)
        self.ipc = IPCClient("face_recognition")
        self.ipc.debug = debug
        
        self.ipc.set_command_listener(self.fr_listener)
        self.ipc.connect(host=ipc_server_host, port=ipc_server_port)

    def shutdown(self):
        print("Shutting down the server...")
        self.ipc.disconnect()

    def fr_listener(self, command: Command):
        if "actions" in command.data:
            for action in command.data["actions"]:
                self.fr_perform_action(command, action)

    def fr_perform_action(self, command_in: Command, action):
        action_type = action["action_type"]
        action_properties = None if "action_properties" not in action else action["action_properties"]
        
        if action_type == "run_recognition_frame":
            # Run the recognition
            fr_data = self.face_recognition.run_recognition_frame(action_properties["img"])
            # Return the result to the request
            command_out = Command(
                data=fr_data,
                to_client_id=command_in.from_client_id
            )
            self.ipc.dispatch_command(command_out)

        elif action_type == "set_unknown_faces":
            # Update the database of informations
            print("Set faces called!")
            try:
                new_faces = self.face_recognition.set_unknown_faces(action_properties["cropped_unknown_faces"])
                # Return the information to the request
                command_out = command_in.gen_response(is_successful=True, data={"new_faces": new_faces})
            except Exception as e:
                command_out = command_in.gen_response(is_successful=False, data={"error": e})
            self.ipc.dispatch_command(command_out)

        elif action_type == "set_unknown_face_threshold":
            self.face_recognition.UNKNOWN_FACE_THRESHOLD = int(action_properties["value"])
            print("Setting unknown threshold to:", int(action_properties["value"]))
            command_out = command_in.gen_response(is_successful=True)
            self.ipc.dispatch_command(command_out)

        elif action_type == "init_face_recognition":
            is_successful=True
            try:
                self.face_recognition.init_state(
                    RESIZE_VALUE=self.face_recognition.RESIZE_VALUE if "resize_value" not in action_properties else int(action_properties["resize_value"]), 
                    UNKNOWN_FACE_THRESHOLD=self.face_recognition.UNKNOWN_FACE_THRESHOLD if "unknown_face_threshold" not in action_properties else int(action_properties["unknown_face_threshold"]),
                )
                print("Setting unknown threshold to:", self.face_recognition.UNKNOWN_FACE_THRESHOLD, "and resize to:", self.face_recognition.RESIZE_VALUE)
            except:
                is_successful=False
            command_out = command_in.gen_response(is_successful=is_successful)
            self.ipc.dispatch_command(command_out)

        elif action_type == "quit":
            self.shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Face Recognition server')
    parser.add_argument('--ipc_server_host', type=str, default='localhost', help='IPC server hostname (default: localhost)')
    parser.add_argument('--ipc_server_port', type=int, default=5001, help='IPC server port number (default: 5001)')
    parser.add_argument('--resize_value', type=int, default=4, help='Face Recognition downscaling (default: 4)')
    parser.add_argument('--unknown_face_threshold', type=int, default=10, help='Face Recognition unknown threshold (see documentation) (default: 10)')
    parser.add_argument('--debug', type=bool, default=False, help='Print debug infos (default: False)')
    args = vars(parser.parse_args())

    fr_server = FaceRecognitionServer(**args)
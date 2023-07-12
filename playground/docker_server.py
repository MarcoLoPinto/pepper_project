import os, sys
from RAIM.ipc_client import IPCClient
from RAIM.ipc_command import Command

from FaceRecognition.fr_system import FaceRecognition
import cv2

# This part will start Face Recognition

ipc_server_host = "localhost"
ipc_server_port = 5001

camera_type = "local" # either "local" (this pc), "robot" or "browser" (not supported)
resize_value = 4 # downscaling the frame captured from camera (+speed, -accuracy)
selected_face = None

class CameraWrapper():
    def __init__(self, cam_type) -> None:
        self.camera = cv2.VideoCapture(0)
    def get_frame(self):
        ret, frame = self.camera.read()
        return frame[:,:,::-1] # bgr -> rgb
    def release(self):
        self.camera.release()

video_capture = CameraWrapper(camera_type)

ipc_fr = IPCClient("face_recognition")
face_recognition = FaceRecognition(RESIZE_VALUE=resize_value)

def shutdown(*args):
    print("Shutting down the script...")
    ipc_fr.disconnect()

def fr_listener(command):
    global selected_face
    if "img" in command.data:
        # Run the recognition
        fr_data = face_recognition.run_recognition_frame(command.data["img"])
        # If the robot didn't select the chosen one
        if selected_face is None:
            # If there is a known face:
            if "known_faces" in fr_data and len(fr_data["known_faces"]) > 0:
                faces = fr_data["known_faces"]
                selected_face_key, selected_face_value = next(iter(faces.items()))
                print("I see a known face! The first one is: ",selected_face_key)
                command = Command(
                    data={
                        "actions": [
                            {
                                "action_type":"say_move",
                                "action_properties": {
                                    "text": "Hi, I remember you! You are %s" %(selected_face_key),
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
                ipc_fr.dispatch_command(command)
                selected_face = selected_face_key
                ipc_fr.set_command_listener(explanation_listener)
            # If there is only unknown faces:
            elif "cropped_unknown_faces" in fr_data and len(fr_data["cropped_unknown_faces"]) > 0:
                print("I see only unknown faces!")
            # If pepper does not see faces:
            else:
                pass

def explanation_listener(command):
    pass

ipc_fr.set_command_listener(fr_listener)
ipc_fr.connect(host=ipc_server_host, port=ipc_server_port)

if camera_type != "local":
    pass
else:
    frame_to_skip = False
    while selected_face is None:
        if not frame_to_skip:
            command = Command(data={"img":video_capture.get_frame()}, to_client_id="browser")
            fr_listener(command)
        frame_to_skip = not frame_to_skip
    video_capture.release()
    cv2.destroyAllWindows()

# Emergency code
# command = Command(
#     data={
#         "action_type":"quit"
#     }, 
#     to_client_id="pepper"
# )
# ipc_fr.dispatch_command(command)
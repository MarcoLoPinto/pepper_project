import face_recognition
import os, sys
import cv2
import numpy as np
import math

from typing import Dict

import base64

def face_confidence(face_distance, treshold=0.6):
    face_range = (1.0 - treshold)
    linear_value = (1.0 - face_distance) / (face_range * 2.0)

    if face_distance > treshold:
        confidence_value = linear_value
    else:
        confidence_value = (
            linear_value + (
                (1.0 - linear_value) * 
                math.pow((linear_value-0.5)*2, 0.2)
            )
        )

    return round(confidence_value * 100, 2)

class FaceRecognition:

    def __init__(self, RESIZE_VALUE = 4, UNKNOWN_FACE_THRESHOLD = 10):
        self.faces_dir = os.path.join( os.path.dirname(os.path.abspath(__file__) ), "faces/")
        self.init_state(RESIZE_VALUE, UNKNOWN_FACE_THRESHOLD)

    def init_state(self, RESIZE_VALUE = 4, UNKNOWN_FACE_THRESHOLD = 10):
        self.RESIZE_VALUE = RESIZE_VALUE
        self.UNKNOWN_FACE_THRESHOLD = UNKNOWN_FACE_THRESHOLD
        # known faces on faces directory
        self.known_face_encodings = []
        self.known_face_names = []

        # all faces detected on the frame
        self.face_locations = []
        self.face_encodings = []
        
        # Idea: UNKNOWN_FACE_THRESHOLD
        # we need to save new faces, but sometimes in a small frame
        # it could potentially detect a face that is known as unknown.
        # To prevent it, we add a threshold.
        # Number of frames to wait before requesting to add an unknown face:

        # Keep track of unknown faces that could be unknown (the key is the index of face_locations and encodings):
        self.possible_unknown_faces = {}
        # Keep track of unknown faces that must be unknown (the value is the index of face_locations and encodings):
        self.unknown_faces = {}
        # Keep track of known faces detected on the frame
        self.known_faces = {}
        # Keep track of frame
        self.frame = None

        self.encode_faces()

    def encode_faces(self):
        """
        Takes all the faces in the "faces" folder (our face database) and populates the lists known_face_encodings and known_face_names.
        The known_face_encoding will be a list of the face recognition model encodings.
        The known_face_names will be a list of strings being the names of each face.
        """
        self.known_face_encodings = []
        self.known_face_names = []
        for image in os.listdir( self.faces_dir ):
            face_image = face_recognition.load_image_file(os.path.join(self.faces_dir, image))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print('known people:',self.known_face_names)

    def filename_to_name(self, filename: str) -> str:
        """Convert the unserscore-separated name to a capitalized name

        Args:
            filename (str): unserscore-separated name

        Returns:
            str: capitalized name
        """
        name_parts = filename.split('.')[0].split('_')
        name = ' '.join([part.capitalize() for part in name_parts])
        return name
    
    def name_to_filename(self, name: str) -> str:
        """Convert the capitalized name to a unserscore-separated name

        Args:
            name (str): capitalized name

        Returns:
            str: unserscore-separated name
        """
        # Convert the name to lowercase and replace spaces with underscores
        filename = name.lower().replace(' ', '_')
        # Add the ".jpg" file extension
        filename += '.jpg'
        return filename
    
    def base64_to_cv2(self, image_data: str):
        """Converts the base64 encoded image to a openCV image

        Args:
            image_data (str): base64 encoded image

        Returns:
            OpenCVImage: openCV image
        """
        # Convert the Base64-encoded image data to a binary string
        binary_data = base64.b64decode(image_data.split(',')[1])
        if not binary_data:
            return None
        # Convert the binary string to a NumPy array
        array_data = np.frombuffer(binary_data, np.uint8)
        # Decode the NumPy array to an OpenCV image
        cv2_image = cv2.imdecode(array_data, cv2.IMREAD_COLOR)
        return cv2_image
    
    def cv2_to_base64(self, image: np.ndarray):
        """Converts the openCV image to a base64 encoded image 

        Args:
            image (np.ndarray): openCV image

        Returns:
            str: base64 encoded image
        """
        # Encode the OpenCV image as a JPEG
        _, jpeg_data = cv2.imencode('.jpeg', image)
        # Convert the JPEG data to a Base64-encoded string
        base64_data = base64.b64encode(jpeg_data).decode('utf-8')
        # Construct the data URL with the Base64-encoded image data
        data_url = 'data:image/jpeg;base64,' + base64_data
        return data_url

    def run_recognition_frame(self, frame):
        self.frame = frame 
        if isinstance(frame, str):
            cv2_rgb = self.base64_to_cv2(frame)
            if cv2_rgb is None: return {"error": "empty_buffer"}
            else: self.frame = cv2_rgb
        rgb_small_frame = cv2.resize(self.frame, (0,0), fx=1.0/self.RESIZE_VALUE, fy=1.0/self.RESIZE_VALUE)
        # rgb_small_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_BGR2RGB) # bgr -> rgb
        # rgb_small_frame = rgb_small_frame[:,:,::-1] # bgr -> rgb

        # Resetting these values each frame
        self.unknown_faces = {}
        self.known_faces = {}

        # Find all faces in current frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        for i, face_encoding in enumerate(self.face_encodings):
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            # Create standard output for face that exists but we don't know anything
            name, confidence = 'Unknown', 0.0

            best_match_idx = None
            try:
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_idx = np.argmin(face_distances)
            except:
                pass

            if best_match_idx != None and matches[best_match_idx]:
                # Adding face to known faces in this frame
                name = self.known_face_names[best_match_idx]
                confidence = face_confidence(face_distances[best_match_idx])
                self.known_faces[self.filename_to_name(name)] = confidence
                # Removing face that was minstakenly detected as unknown
                if i in self.possible_unknown_faces: 
                    del self.possible_unknown_faces[i]

            else: # Adding code for saving unknown faces!
                if i in self.possible_unknown_faces:
                    self.possible_unknown_faces[i] += 1
                    if self.possible_unknown_faces[i] >= self.UNKNOWN_FACE_THRESHOLD:
                        self.possible_unknown_faces[i] = self.UNKNOWN_FACE_THRESHOLD+1
                        self.unknown_faces[i] = True
                else: 
                    self.possible_unknown_faces[i] = 1
                
        for i in self.possible_unknown_faces.keys():
            if i not in range(len(self.face_encodings)):
                self.possible_unknown_faces[i] = 1

        return {"known_faces": self.known_faces, "cropped_unknown_faces": self.get_cropped_unknown_faces()}
    
    def get_cropped_unknown_faces(self, convert_to_base64 = True):
        cropped_unknown_faces = {}
        for key, value in self.unknown_faces.items():
            (top, right, bottom, left) = self.face_locations[key]
            top *= self.RESIZE_VALUE
            right *= self.RESIZE_VALUE
            bottom *= self.RESIZE_VALUE
            left *= self.RESIZE_VALUE

            cropped_unknown_face = self.frame[top:bottom, left:right]
            if convert_to_base64:
                cropped_unknown_face = self.cv2_to_base64(cropped_unknown_face)

            cropped_unknown_faces[key] = cropped_unknown_face

        return cropped_unknown_faces
    
    def set_unknown_faces(self, setted_faces: Dict[int, str]):
        new_faces = []
        for key, name in setted_faces.items():
            key = int(key)
            if len(self.face_locations) > key:
                (top, right, bottom, left) = self.face_locations[key]
                top *= self.RESIZE_VALUE
                right *= self.RESIZE_VALUE
                bottom *= self.RESIZE_VALUE
                left *= self.RESIZE_VALUE

                cropped_unknown_face = self.frame[top:bottom, left:right]
                filename = self.name_to_filename(name)
                cv2.imwrite(os.path.join(self.faces_dir,filename), cropped_unknown_face) # Save the new face image in the faces folder
                del self.unknown_faces[key]
                new_faces.append(self.filename_to_name(filename))
        self.encode_faces()
        return new_faces



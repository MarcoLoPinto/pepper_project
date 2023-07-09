import face_recognition
import os, sys
import cv2
import numpy as np
import math
import copy

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

    return str(round(confidence_value * 100, 2)) + '%'

class FaceRecognition:
    # known faces on faces directory
    known_face_encodings = []
    known_face_names = []

    # all faces detected on the frame
    face_locations = []
    face_encodings = []
    
    # Idea: UNKNOWN_FACE_THRESHOLD
    # we need to save new faces, but sometimes in a small frame
    # it could potentially detect a face that is known as unknown.
    # To prevent it, we add a threshold.
    # Number of frames to wait before requesting to add an unknown face:

    # Keep track of unknown faces that could be unknown (the key is the index of face_locations and encodings):
    possible_unknown_faces = {}
    # Keep track of unknown faces that must be unknown (the value is the index of face_locations and encodings):
    unknown_faces = {}
    # Keep track of known faces detected on the frame
    known_faces = {}

    def __init__(self, RESIZE_VALUE = 4, FRAMES_TO_SKIP = 0, UNKNOWN_FACE_THRESHOLD = 10):
        self.encode_faces()
        self.RESIZE_VALUE = RESIZE_VALUE
        self.FRAMES_TO_SKIP = FRAMES_TO_SKIP # number of frames to skip each time
        self.skipped_frames = FRAMES_TO_SKIP # number of frames skipped
        self.UNKNOWN_FACE_THRESHOLD = UNKNOWN_FACE_THRESHOLD

    def encode_faces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        for image in os.listdir('./faces'):
            face_image = face_recognition.load_image_file('./faces/%s' %(image))
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print('known people:',self.known_face_names)

    def filename_to_name(self, filename):
        name_parts = filename.split('.')[0].split('_')
        name = ' '.join([part.capitalize() for part in name_parts])
        return name

    def run_recognition_frame(self, frame):
        small_frame = cv2.resize(frame, (0,0), fx=1.0/self.RESIZE_VALUE, fy=1.0/self.RESIZE_VALUE)
        rgb_small_frame = small_frame[:,:,::-1] # bgr -> rgb

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

            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_idx = np.argmin(face_distances)

            if matches[best_match_idx]:
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
                        self.unknown_faces[i] = True
                else: self.possible_unknown_faces[i] = 1

        return self.known_faces, self.unknown_faces


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()


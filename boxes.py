import face_recognition
import cv2
import numpy as np
import os, sys
import math

font_scale = 2e-3
thickness_scale = 1e-3

def optimal_font_dims(img, font_scale , thickness_scale):
    """
    Get optimal font dimensions for the given image
    :param img: Image to get the optimal font dimensions
    :param font_scale:
    :param thickness_scale:
    :return:
    """
    h, w, _ = img.shape
    font_scale = min(w, h) * font_scale
    thickness = math.ceil(min(w, h) * thickness_scale)
    return font_scale, thickness

def face_confidence(face_distance, face_match_threshold=0.4):
    """
    Get the confidence of the face
    :param face_distance: Distance between the face and the known face
    :param face_match_threshold: Threshold to consider a face as a match
    :return: Confidence of the face
    """
    rango = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (rango * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    """
    Class to recognize faces

    """
    face_locations = []
    face_encodings = []
    face_names = []
    faces_confidences = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    global font_scale
    global thickness_scale



    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        """

        :return:
        """
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f'faces/{image}')
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

        print(self.known_face_names)

    def run_recognition(self):
        """
        Process the video and recognize the faces
        :return:
        """
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('No se pudo abrir la cámara')

        while True:
            ret, frame = video_capture.read()

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find all faces in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Desconocido"
                    confidence = "0%"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]: # Find a match
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                        name_without_extension, _ = os.path.splitext(name)

                        self.face_names.append(name_without_extension)
                        self.faces_confidences.append(confidence)
                    else:
                        self.face_names.append(name)

            self.process_current_frame = not self.process_current_frame

            # Display annotations in the video
            for (x, y, w, h), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                x *= 4
                y *= 4
                w *= 4
                h *= 4


                # Get optimal font dimensions
                font_scale = 5e-4
                thickness_scale = 7.5e-4
                font_scale, thickness = optimal_font_dims(frame, font_scale, thickness_scale)


                # Change color box depending on the name
                if name == 'Desconocido' or confidence < '70.0%':
                    color_box = (0, 0, 255) # Red
                    acceso_text = "ACCESO DENEGADO"
                elif confidence >= '70.0%':
                    color_box = (72, 131, 72) # Green
                    acceso_text = "ACCESO PERMITIDO"

                # draw a rectangle around the face
                cv2.rectangle(frame, (h, x), (y, w), color_box, 2)
                # draw a filled rectanle below the face
                cv2.rectangle(frame, (h, w + 1), (y, w + 100), color_box, -1)

                font = cv2.FONT_HERSHEY_DUPLEX
                name_text = f"{name}"
                confidence_text = f"{confidence}"
                cv2.putText(frame, name_text, (h + 6, w + 20), font, font_scale, (255, 255, 255), thickness)
                if name != 'Desconocido' and confidence >= '70.0%':
                    cv2.putText(frame, confidence_text, (h + 6, w + 55), font, font_scale, (255, 255, 255), thickness)
                    cv2.putText(frame, acceso_text, (h + 6, w + 90), font, font_scale, (255, 255, 255), thickness)
                else:
                    cv2.putText(frame, acceso_text, (h + 6, w + 90), font, font_scale, (255, 255, 255), thickness)


            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()
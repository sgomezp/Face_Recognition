import threading
import cv2
from deepface import DeepFace
from mtcnn.mtcnn import MTCNN
import os
import time
from deepface.commons import functions

def check_face(frame):
    global recognized_person
    global data

    for person_name, photos in data.items():
        for photo_path in photos:
            try:
                reference_image = cv2.imread(photo_path)
                reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)

                # Antes de la verificación
                frame_normalized = functions.extract_faces(frame)
                reference_image_normalized = functions.extract_faces(reference_image)

                result = DeepFace.verify(frame_normalized, reference_image_normalized, distance_metric="cosine")

                if result['verified']:
                    print("Persona reconocida")
                    recognized_person = person_name
                    confidence = 1 - result['distance']
                    return recognized_person, confidence  # Exit the function when a face is recognized
            except ValueError:
                pass

    recognized_person = "Desconocido"
    confidence = 0
    return recognized_person, confidence
def count_photos(dir, extension):
    try:
        files = os.listdir(dir)
        files_with_ext = [file for file in files if file.endswith(extension)]
        total_files = len(files_with_ext)
        return total_files
    except Exception as e:
        print(f"Error al contar archivos: {str(e)}")
        return None

def detect_faces(frame):
    try:
        faces = mtcnn.detect_faces(frame)
        return faces
    except Exception as e:
        print(f"Error in face detection: {e}")
        return []

# Max number of photos to take
max_photos = 50

# Load MTCNN model for face detection
mtcnn = MTCNN()

counter = 0

# Directory to save photos
output_base_dir = "data"
recognized_person = 'Desconocido'

# Load photo routes for each person
data = {}
root_dir = 'data'

for person_name in os.listdir(root_dir):
    person_dir = os.path.join(root_dir, person_name)

    if os.path.isdir(person_dir):
        photos = [os.path.join(person_dir, photo) for photo in os.listdir(person_dir) if photo.endswith('.jpg')]
        data[person_name] = photos
        print(f"Photos of {person_name}: {len(photos)}")

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 1280, 720)

while True:
    ret, frame = cap.read()
    if ret:
        try:
            # Detect faces with MTCNN
            faces = detect_faces(frame)
            print(f"Número de caras: {len(faces)}")
        except Exception as e:
            print(f"Error in face detection: {e}")


        for face in faces:
            x, y, w, h = face['box']
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)

            if counter % 60 == 0:
                try:
                    recognized_person, confidence = check_face(frame[y:y + h, x:x + w].copy())
                    threading.Thread(target=check_face, args=(frame[y:y + h, x:x + w].copy(),)).start()

                except ValueError:
                    pass
            counter += 1

            if recognized_person != 'Desconocido':
                saved_photos = count_photos(os.path.join(output_base_dir, recognized_person), '.jpg')
                roi = frame[y:y + h, x:x + w]

                if saved_photos < max_photos:
                    timestamp = int(time.time())
                    unique_identifier = f"{recognized_person.upper()}_{timestamp}"
                    output_dir = os.path.join(output_base_dir, recognized_person)

                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)

                    output_path = os.path.join(output_dir, f'{unique_identifier}_roi_{saved_photos}.jpg')
                    cv2.imwrite(output_path, roi)
                    saved_photos += 1

                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (72, 131, 72), 3)
                cv2.putText(frame, f"{recognized_person.upper()}", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 255), 2)
                cv2.putText(frame, "ACCESO PERMITIDO", (x, y + h + 75), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (72, 131, 72), 2)
                cv2.putText(frame, f"Seguridad: {confidence:.2%}", (x, y + h + 110), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 255), 2)
            else:
                cv2.putText(frame, f"{recognized_person.upper()}", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255), 2)
                cv2.putText(frame, "ACCESO DENEGADO", (x, y + h + 75), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (0, 0, 255), 2)

        cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

import cv2
import numpy as np
import time
import os
import threading
import cv2
from deepface import DeepFace

counter = 0

def check_face(frame):
    global recognized_person
    global data

    for person_name, photos in data.items():
        for photo_path in photos:
            try:
                reference_image = cv2.imread(photo_path)
                reference_image = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)

                result = DeepFace.verify(frame, reference_image, distance_metric = "cosine")

                if result['verified']:
                    recognized_person = person_name
                    confidence = 1 - result['distance']
                    return recognized_person, confidence # Exit the function when a face is recognized
            except ValueError:
                pass

    recognized_person = "Desconocido"
    confidence = 0
    return recognized_person, confidence

def count_photos(dir, extension):
    try:
        # list all files in the directory
        files = os.listdir(dir)

        # Filter the files with the extension specified
        files_with_ext = [file for file in files if file.endswith(extension)]

        # Count the number of files with the extension specified
        total_files = len(files_with_ext)

        return total_files

    except Exception as e:
        print(f"Error al contar archivos: {str(e)}")
        return None



# Configuración de YOLO
yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
yolo_layers = yolo_net.getUnconnectedOutLayersNames()

# Configuración de confianza y umbral de no máxima supresión (NMS)
confidence_threshold = 0.5
nms_threshold = 0.4

# Directorio base para guardar las fotos
output_base_dir = "data"
recognized_person = 'Desconocido'

# load photos route for each person
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

# Establece el tamaño de la ventana manualmente
cv2.namedWindow('video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('video', 1280, 720)

while True:
    ret, frame = cap.read()
    if ret:
        # Obtener las dimensiones del frame
        height, width, channels = frame.shape


        # Detección de objetos con YOLO
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(blob)
        detections = yolo_net.forward(yolo_layers)

        # Procesar las detecciones
        for detection in detections:
            for obj in detection:
                scores = obj[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > confidence_threshold and class_id == 0:  # 0 para la clase "persona"
                    box = obj[0:4] * np.array([width, height, width, height])
                    (x, y, w, h) = box.astype("int")

                    # Ajustar las coordenadas de la caja delimitadora
                    x = max(0, x)
                    y = max(0, y)
                    x = min(x, width - 1)
                    y = min(y, height - 1)

                    # Dibujar rectángulo alrededor de la cara
                    frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                    if counter % 60 == 0:
                        try:
                            recognized_person, confidence = check_face(frame[y:y + h, x:x + w])
                            threading.Thread(target=check_face, args=(frame[y:y + h, x:x + w],)).start()
                        except ValueError:
                            pass
                    counter += 1

                    # Resto del código sigue igual...
                    if recognized_person != 'Desconocido':  # and confidence > 0.8:
                        # Count the number of photos saved
                        # saved_photos = count_photos(os.path.join(output_base_dir, recognized_person), '.jpg')
                        # save the ROI
                        roi = frame[y:y + h, x:x + w]
                        # create a file with the ROI
                        # if saved_photos < max_photos: #and confidence > 0.8:
                        #     timestamp = int(time.time())
                        #     unique_identifier = f"{recognized_person.upper()}_{timestamp}"
                        #     output_dir = os.path.join(output_base_dir, recognized_person)
                        #     # Verify if the directory exists and create it if not
                        #     if not os.path.exists(output_dir):
                        #         os.makedirs(output_dir)
                        #
                        #     output_path = os.path.join(output_dir, f'{unique_identifier}_roi_{saved_photos}.jpg')
                        #     cv2.imwrite(output_path, roi)
                        #     saved_photos += 1

                        # draw a rectangle around the faces with border green
                        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (72, 131, 72), 3)
                        cv2.putText(
                            frame,
                            f"{recognized_person.upper()}",
                            (x, y + h + 40),  # display name below the bounding box
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (255, 255, 255),  # text color
                            2
                        )

                        cv2.putText(
                            frame,
                            "ACCESO PERMITIDO",
                            (x, y + h + 75),  # display below the name
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (72, 131, 72),  # text color
                            2
                        )

                        cv2.putText(
                            frame,
                            f"Seguridad: {confidence:.2%}",
                            (x, y + h + 110),  # display below Access Allowed
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (255, 255, 255),  # text color
                            2
                        )
                    else:
                        cv2.putText(
                            frame,
                            f"{recognized_person.upper()}",
                            (x, y + h + 40),  # display 'Desconocido' below the bounding box
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 0, 255),  # text color
                            2
                        )

                        cv2.putText(
                            frame,
                            "ACCESO DENEGADO",
                            (x, y + h + 75),  # Display below 'Desconocido'
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 0, 255),  # text color
                            2
                        )



        cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

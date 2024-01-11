import streamlit as st
import numpy as np
import os
import cv2


faces_folder = "./faces"

st.title("Registro en el sistema")

st.write("Para poder acceder al sistema, necesitamos que te registres. Para ello, necesitamos que nos des una foto de tu rostro")

picture = st.camera_input("Toma una foto de tu rostro")
# Guardar la captura en la carpeta temporal



if picture:
    st.image(picture, caption="Tu foto", use_column_width=True)
    foto_ok = st.radio("¿Quieres guardar esta foto?", ("Sí", "No"), index=None, key=None)
    if foto_ok == "Sí":
        name = st.text_input("Tu nombre, por favor:")
        file_name = f"{name}.jpg"
        image_path = os.path.join(faces_folder, file_name)

        # Read the image data from the picture variable
        picture_data = np.frombuffer(picture.read(), np.uint8)

        # Decode the image data
        picture_img = cv2.imdecode(picture_data, cv2.IMREAD_COLOR)

        # Save the image
        cv2.imwrite(image_path, picture_img)

        st.write(f"{name} tu foto se ha guardado con tu nombre. Ya puedes ir a la pestaña de reconocimiento facial")
    else:
        st.write("No se ha guardado la foto. Puedes tomar otra foto")

import streamlit as st
import numpy as np
import os
import cv2

faces_folder = "./faces"

st.title("Registro en el sistema")

st.write("Para poder acceder al sistema, necesitamos que te registres. Para ello, necesitamos que nos des una foto de tu rostro")

# Estado de la aplicación
state = st.session_state
if not hasattr(state, 'photo_form_submitted'):
    state.photo_form_submitted = False
if not hasattr(state, 'name_form_submitted'):
    state.name_form_submitted = False

picture = st.camera_input("Toma una foto de tu rostro")

if picture:
    st.image(picture, caption="Tu foto", use_column_width=True)

    with st.form(key='photo_form'):
        foto_ok = st.radio("¿Quieres guardar esta foto?", ("Sí", "No"))
        submit_button_photo = st.form_submit_button(label='Confirmar')

    if submit_button_photo and foto_ok == "No":
        st.write("No se ha guardado la foto. Puedes tomar otra foto")
    elif submit_button_photo and foto_ok == "Sí":
        state.photo_form_submitted = True

if state.photo_form_submitted:
    with st.form(key='name_form'):
        name = st.text_input("Tu nombre, por favor:")
        submit_button_name = st.form_submit_button(label='Confirmar')

    if submit_button_name and name == "":
        st.write("No has introducido tu nombre")
    elif submit_button_name:
        state.name_form_submitted = True
        file_name = f"{name}.jpg"
        st.write(f"file_name: {file_name}")
        image_path = os.path.join(faces_folder, file_name)

        # Resto del código para guardar la imagen...
        picture_data = np.frombuffer(picture.read(), np.uint8)
        picture_img = cv2.imdecode(picture_data, cv2.IMREAD_COLOR)
        cv2.imwrite(image_path, picture_img)

        st.write(f"{name}, gracias por registrarte")

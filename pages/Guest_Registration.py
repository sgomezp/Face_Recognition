import time
import streamlit as st
import numpy as np
import os
import cv2
from streamlit_extras.switch_page_button import switch_page
import pyautogui


# Inicialización de variables
faces_folder = "./faces"


st.title("System Registration Page")

st.write("To access the system, we need you to register. For this, we require a photo of your face")

# Estado de la aplicación
state = st.session_state
if not hasattr(state, 'photo_form_submitted'):
    state.photo_form_submitted = False
if not hasattr(state, 'name_form_submitted'):
    state.name_form_submitted = False

def reset_state():
    state.photo_form_submitted = False
    state.name_form_submitted = False


# Botón para reiniciar
if st.button("Restart Page", on_click=reset_state, key= "reset_1"):
    pyautogui.hotkey("ctrl", "F5")


picture = st.camera_input("Take a photo of your face")

if picture:
    st.image(picture, caption="Your photo", use_container_width=True)

    with st.form(key='photo_form'):
        foto_ok = st.radio("Do you want to save this photo?", ("Yes", "No"))
        submit_button_photo = st.form_submit_button(label='Confirm')

    if submit_button_photo and foto_ok == "No":
        st.write("The photo was not saved. You can take another photo")
    elif submit_button_photo and foto_ok == "Yes":
        reset_state()
        state.photo_form_submitted = True

if state.photo_form_submitted:
    with st.form(key='name_form'):
        name = st.text_input("Your name, please:")
        submit_button_name = st.form_submit_button(label='Confirm')

    if submit_button_name and name == "":
        st.write("You haven't entered your name")
    elif submit_button_name:
        reset_state()
        state.name_form_submitted = True
        file_name = f"{name}.jpg"
        image_path = os.path.join(faces_folder, file_name)

        # convert image to numpy array uint8
        picture_data = np.frombuffer(picture.read(), np.uint8)
        # decode image
        picture_img = cv2.imdecode(picture_data, cv2.IMREAD_COLOR)
        # save image
        cv2.imwrite(image_path, picture_img)

        container = st.empty()
        container.success(f"{name}, thank you for registering. You can now try again on the Facial Recognition page")
        time.sleep(2)
        container.empty()
        switch_page("Face Recognition")


# Botón para reiniciar
if st.button("Restart Page", on_click=reset_state, key= "reset_2"):
    pyautogui.hotkey("ctrl", "F5")



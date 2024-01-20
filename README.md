# Facial Recognition Project through Computer Vision


### Personal version of the [team-developed project](https://github.com/AI-School-F5-P2/Face_Recognition_5.git), using Streamlit as a graphical interface.
## Problem Statement:

The company is hosting a significant event and has tasked its two leading artificial intelligence (AI) experts with 
developing a facial recognition system using Computer Vision. The objective is to streamline the event entry process 
by eliminating the need for ticket verification and ID checks. The proposal involves employees approaching a laptop, 
where an AI-based system will recognize their faces in real-time, granting or denying access.

The request entails implementing a machine learning system that, through a camera, can determine whether the person 
in front of the device is an employee or not. It is crucial to note that external data is not available, requiring 
the AI experts to generate the necessary dataset. Before deploying the system in production, a test is required to 
ensure accurate recognition of team members (developers). It is worth mentioning that both the model and the data must 
run on a laptop, and the use of cloud services is not allowed due to privacy considerations.

## The Solution:

To address this issue, the programming language Python has been employed, along with the libraries OpenCV and 
face_recognition. A facial recognition model has been developed and trained using images of the company's employees. 
Upon initiating the program, the real-time camera is activated, and upon detecting the presence of one or more 
employees in front of it, the system automatically proceeds to identify their faces, determining whether they are 
authorized to access the event.

The program compares the captured face with images of employees stored in the system. In the case of a successful 
recognition, the employee's name and confidence percentage are displayed below the identified face on the screen. 
Entry is guaranteed if this percentage is equal to or higher than 70%. The visual indication "ACCESS GRANTED" is 
presented in these instances. On the other hand, if the face is not recognized, the bounding box is highlighted in 
red, and the message "Unknown - ACCESS DENIED" is displayed, indicating the prohibition of access.

If the employee has not been previously registered in the system, they have the opportunity to do so. They will be 
prompted to take a photograph of themselves. Once the image is captured, it is displayed on the screen, and the user 
is asked if they want to save it. If the response is affirmative, they will also be prompted to enter their name. 
Once the image is captured along with the name, it is stored in the system. If the user is not satisfied with the 
image, they will be asked to take another photograph, and the process is repeated.

The program allows for the registration of an unlimited number of employees and can be executed as many times as 
necessary. The facial recognition model is automatically trained each time the program runs, using the images of the 
employees stored in the system. This ensures that the model is consistently updated, enabling the recognition of all 
registered employees' faces.

## File Structure Description:
- **.gitignore**: File containing the list of files that will not be uploaded to the repository.
- **faces**: Folder containing images of employees and test images.
- **Reconocimiento_Facial.py**: File containing the main code of the project.
- **Registro_invitados.py**: File containing the code for registering guests.
- **README.md**: File containing the project description.
- **requirements.txt**: File containing the project dependencies.
 
## Usage Instructions::
1. Clone the repository. [Link](.....)
2. Navigate to your project directory.
3. Optional, but highly recommended: create a virtual environment.
4. Upload the images of the employees to the "faces" folder.
5. Install the required dependencies by executing the following command:
```
pip install -r requirements.txt
```
5. Execute the file Reconocimiento_Facial.py with the following command:
```
streamlit run Reconocimiento_Facial.py
```

## Observations:
- If you are using Windows, you need to install [Visual Studio](https://visualstudio.microsoft.com/) with C++ tools.
- Additionally, CMake must be installed.
- Next, install dlib with the following command:
```
pip install dlib
```
-Following the installation of face_recognition:
```
pip install face_recognition
```
## Future Improvements:
- Implement a logging system to keep a record of accesses.
- Integrate a voice recognition system to identify employees.
- Implement a fingerprint recognition system to identify employees.
- Dockerize the application.

## References:
- [Face_recognition library](https://github.com/ageitgey/face_recognition?tab=readme-ov-file)
- [OpenCV](https://opencv.org/)
- [Streamlit](https://streamlit.io/)
- [Streamlit-Extras](https://arnaudmiribel.github.io/streamlit-extras/)
 

  




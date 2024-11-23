# Face Detection App README

## Overview
The **Face Detection App** is a Python application designed to detect faces in images or in real-time via a webcam. It utilizes the **MediaPipe** library for face detection and **Tkinter** for the graphical user interface.

---

## Features
1. **Image Detection**:  
   - Upload an image and detect faces within it.  
   - Detected faces are highlighted directly on the image.

2. **Webcam Detection**:  
   - Use your webcam to detect faces in real-time.  
   - Results are displayed live with face annotations.

3. **Simple Interface**:  
   - Intuitive GUI with mode selection for ease of use.  

---

## Dependencies
To run the application, you need the following Python libraries:
- `tkinter` (default with Python)
- `opencv-python`  
- `mediapipe`  
- `numpy`  
- `Pillow`

You can install the dependencies using pip:
```bash
pip install opencv-python mediapipe numpy Pillow
```

---

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Run the script:
   ```bash
   python script.py
   ```
3. Select a mode:
   - **Image Detection**: Choose an image file from your computer.
   - **Webcam Detection**: Start live face detection via your webcam.

---

## File Structure
- `script.py`: The main application script.

---

## Known Issues
- Webcam functionality requires access to a compatible camera.
- For high-resolution images, detection might take longer.
- Ensure the webcam is not being used by another application before launching.

---

## Contributions
Feel free to contribute to the project! Fork the repository, make your changes, and submit a pull request.

---

## License
This project is licensed under the MIT License.

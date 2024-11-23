import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")
        self.root.geometry("800x600")

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.create_mode_selection()

    def create_mode_selection(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Choose Detection Mode", 
                 font=("Helvetica", 16)).pack(pady=20)

        image_btn = tk.Button(self.main_frame, text="Image Detection", 
                               command=self.start_image_detection,
                               width=30, height=3)
        image_btn.pack(pady=10)

        webcam_btn = tk.Button(self.main_frame, text="Webcam Detection", 
                                command=self.start_webcam_detection,
                                width=30, height=3)
        webcam_btn.pack(pady=10)

    def start_image_detection(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        
        if not file_path:
            self.create_mode_selection()
            return

        try:
            image = cv2.imread(file_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Face detection
            with self.mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5) as face_detection:
                
                results = face_detection.process(image_rgb)

                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(image, detection)

            pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(pil_img)

            image_label = tk.Label(self.main_frame, image=photo)
            image_label.image = photo
            image_label.pack(expand=True)

            back_btn = tk.Button(self.main_frame, text="Back to Mode Selection", 
                                 command=self.create_mode_selection)
            back_btn.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Could not process image: {str(e)}")
            self.create_mode_selection()

    def start_webcam_detection(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        webcam_label = tk.Label(self.main_frame)
        webcam_label.pack(expand=True, fill=tk.BOTH)

        back_btn = tk.Button(self.main_frame, text="Stop Webcam", 
                             command=self.create_mode_selection)
        back_btn.pack(pady=10)

        # Webcam capture
        cap = cv2.VideoCapture(0)

        def update_frame():
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                cap.release()
                self.create_mode_selection()
                return

            # Face detection
            with self.mp_face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5) as face_detection:
                
                # Process frame
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(frame_rgb)

                # Draw detections if faces found
                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(frame, detection)

            # Convert frame to PhotoImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(pil_img)

            # Update label
            webcam_label.configure(image=photo)
            webcam_label.image = photo

            # Schedule next update
            webcam_label.after(10, update_frame)

        # Start updating frames
        update_frame()

def main():
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# 
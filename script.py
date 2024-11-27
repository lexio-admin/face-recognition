import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import mediapipe as mp
from PIL import Image, ImageTk


class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f4f4f4")

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils

        self.main_frame = tk.Frame(root, bg="#f4f4f4")
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        self.create_mode_selection()

    def create_mode_selection(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Choose Detection Mode",
                 font=("Helvetica", 18, "bold"), bg="#f4f4f4").pack(pady=20)

        tk.Button(self.main_frame, text="Image Detection",
                  command=self.start_image_detection,
                  width=30, height=2, bg="#007acc", fg="white", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(self.main_frame, text="Video Detection",
                  command=self.start_video_detection,
                  width=30, height=2, bg="#007acc", fg="white", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(self.main_frame, text="Webcam Detection",
                  command=self.start_webcam_detection,
                  width=30, height=2, bg="#007acc", fg="white", font=("Helvetica", 14)).pack(pady=10)

    def start_image_detection(self):
        self.clear_frame()
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

            with self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
                results = face_detection.process(image_rgb)

                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(image, detection)

            self.display_image(image)

        except Exception as e:
            messagebox.showerror("Error", f"Could not process image: {str(e)}")
            self.create_mode_selection()

    def start_video_detection(self):
        self.clear_frame()
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if not file_path:
            self.create_mode_selection()
            return

        cap = cv2.VideoCapture(file_path)

        video_label = tk.Label(self.main_frame)
        video_label.pack(expand=True, fill=tk.BOTH)

        back_btn = tk.Button(self.main_frame, text="Back to Mode Selection",
                             command=lambda: self.stop_capture(cap),
                             bg="#007acc", fg="white", font=("Helvetica", 12))
        back_btn.pack(pady=10)

        def process_frame():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                self.create_mode_selection()
                return

            with self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(frame_rgb)

                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(frame, detection)

            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(pil_img)

            video_label.config(image=photo)
            video_label.image = photo
            video_label.after(10, process_frame)

        process_frame()

    def start_webcam_detection(self):
        self.clear_frame()
        webcam_label = tk.Label(self.main_frame)
        webcam_label.pack(expand=True, fill=tk.BOTH)

        cap = cv2.VideoCapture(0)

        back_btn = tk.Button(self.main_frame, text="Back to Mode Selection",
                             command=lambda: self.stop_capture(cap),
                             bg="#007acc", fg="white", font=("Helvetica", 12))
        back_btn.pack(pady=10)

        def update_frame():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                self.create_mode_selection()
                return

            with self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detection.process(frame_rgb)

                if results.detections:
                    for detection in results.detections:
                        self.mp_drawing.draw_detection(frame, detection)

            pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(pil_img)

            webcam_label.config(image=photo)
            webcam_label.image = photo
            webcam_label.after(10, update_frame)

        update_frame()

    def stop_capture(self, cap):
        cap.release()
        self.create_mode_selection()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def display_image(self, image):
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        photo = ImageTk.PhotoImage(pil_img)

        image_label = tk.Label(self.main_frame, image=photo)
        image_label.image = photo
        image_label.pack(expand=True)

        back_btn = tk.Button(self.main_frame, text="Back to Mode Selection",
                             command=self.create_mode_selection,
                             bg="#007acc", fg="white", font=("Helvetica", 12))
        back_btn.pack(pady=10)


def main():
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

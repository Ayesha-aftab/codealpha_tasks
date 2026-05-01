import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
from ultralytics import YOLO

# Global Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AIVisionDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("CodeAlpha | AI Vision Control Center")
        self.geometry("1200x750")
        self.configure(fg_color="#0f0f10") # Deep tech black background

        # --- AI Engine Setup ---
        self.model = YOLO('yolov8n.pt')
        self.cap = None
        self.is_running = False

        # --- Main Layout Structure ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 1. Elegant Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#161618")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="VISION AI", 
                                      font=ctk.CTkFont(family="Orbitron", size=24, weight="bold"),
                                      text_color="#3b82f6")
        self.logo_label.pack(pady=(40, 10))
        
        self.sub_logo = ctk.CTkLabel(self.sidebar, text="Object Tracking System", 
                                    font=ctk.CTkFont(size=12), text_color="gray")
        self.sub_logo.pack(pady=(0, 40))

        # Action Buttons with custom colors
        self.btn_webcam = ctk.CTkButton(self.sidebar, text="START LIVE FEED", 
                                       command=self.start_webcam, 
                                       height=45, corner_radius=8,
                                       fg_color="#3b82f6", hover_color="#2563eb",
                                       font=ctk.CTkFont(weight="bold"))
        self.btn_webcam.pack(pady=12, padx=20)

        self.btn_image = ctk.CTkButton(self.sidebar, text="ANALYZE IMAGE", 
                                      command=self.upload_image, 
                                      height=45, corner_radius=8,
                                      fg_color="#27272a", hover_color="#3f3f46",
                                      border_width=1, border_color="#3b82f6")
        self.btn_image.pack(pady=12, padx=20)

        self.btn_stop = ctk.CTkButton(self.sidebar, text="SHUTDOWN", 
                                     command=self.stop_session, 
                                     height=40, corner_radius=8,
                                     fg_color="#7f1d1d", hover_color="#b91c1c")
        self.btn_stop.pack(pady=20, padx=20, side="bottom")

        # --- 2. Central Vision Screen ---
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=1, padx=30, pady=20, sticky="nsew")

        # Visual Screen Container
        self.screen_border = ctk.CTkFrame(self.main_view, fg_color="#1e1e20", corner_radius=15, border_width=2, border_color="#27272a")
        self.screen_border.pack(expand=True, fill="both")

        self.video_label = ctk.CTkLabel(self.screen_border, text="AWAITING INPUT SIGNAL...", 
                                       font=ctk.CTkFont(size=16), text_color="#52525b")
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # --- 3. Intelligence Panel (Right Sidebar) ---
        self.intel_panel = ctk.CTkFrame(self, width=300, fg_color="#161618", corner_radius=0)
        self.intel_panel.grid(row=0, column=2, sticky="nsew")

        self.intel_title = ctk.CTkLabel(self.intel_panel, text="LIVE ANALYSIS", 
                                       font=ctk.CTkFont(size=14, weight="bold"), text_color="#3b82f6")
        self.intel_title.pack(pady=(30, 10))

        self.obj_list = ctk.CTkTextbox(self.intel_panel, width=260, height=550, 
                                      fg_color="#0f0f10", border_color="#27272a", border_width=1,
                                      font=("Courier New", 13), text_color="#10b981")
        self.obj_list.pack(pady=10, padx=20)
        self.obj_list.insert("0.0", "> System Ready\n> Waiting for Stream...")

        # --- 4. Footer (The Professional Touch) ---
        self.footer = ctk.CTkFrame(self, height=40, fg_color="#111113", corner_radius=0)
        self.footer.grid(row=1, column=0, columnspan=3, sticky="ew")
        
        self.credits = ctk.CTkLabel(self.footer, text="Created by Ayesha Aftab | AI Internship Project 2026", 
                                   font=ctk.CTkFont(size=12, slant="italic"), text_color="#71717a")
        self.credits.pack(pady=5)

    def start_webcam(self):
        self.stop_session()
        self.cap = cv2.VideoCapture(0)
        self.is_running = True
        self.obj_list.delete("0.0", "end")
        self.obj_list.insert("0.0", "> Initializing Webcam...\n")
        self.process_loop()

    def upload_image(self):
        self.stop_session()
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
        if path:
            img = cv2.imread(path)
            results = self.model(img)
            self.display_results(results[0], img)
            self.obj_list.insert("end", f"\n> Image Uploaded: {path.split('/')[-1]}")

    def stop_session(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.video_label.configure(image=None, text="SIGNAL LOST")
        self.obj_list.insert("end", "\n> Session Terminated.")

    def process_loop(self):
        if self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                results = self.model.track(frame, persist=True, conf=0.4)
                self.display_results(results[0], frame)
                self.after(10, self.process_loop)

    def display_results(self, result, frame):
        # AI Overlay
        annotated_frame = result.plot()
        rgb_img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # Displaying the image in the UI
        img_pil = Image.fromarray(rgb_img)
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(720, 540))
        
        self.video_label.configure(image=img_ctk, text="")
        
        # Updating the Analysis Box
        self.obj_list.delete("0.0", "end")
        self.obj_list.insert("0.0", f"> FRAME ACTIVE\n{'-'*20}\n")
        
        names = self.model.names
        for box in result.boxes:
            name = names[int(box.cls[0])]
            conf = float(box.conf[0])
            self.obj_list.insert("end", f"DETECTED: {name.upper()}\nCONF: {conf:.2%}\n{'-'*20}\n")

if __name__ == "__main__":
    app = AIVisionDashboard()
    app.mainloop()

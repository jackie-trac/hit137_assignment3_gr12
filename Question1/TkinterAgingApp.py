import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import threading
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES  # Inheritance: TkinterDnD inherits from tkinter.Tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import ttk  # For the progress bar 

class FaceAgingApp(TkinterDnD.Tk):  # Inheritance: FaceAgingApp inherits from TkinterDnD
    def __init__(self):
        super().__init__()  # Initialize the parent TkinterDnD
        self.title("AI Face Aging App using Fast-AgingGAN")
        self.geometry("800x600")
        self.config(bg="#2e2e2e")

        self.create_widgets()  # Encapsulation: Hide widget creation complexity
        self.setup_drag_and_drop()  # Separate method to set up drag-and-drop

    def create_widgets(self): #Encapsulation: Create and configure all the widgets.
        # Frame for drag and drop
        self.drop_frame = tk.Frame(self, width=280, height=150, bg="#444", relief="solid", bd=2, highlightthickness=2)
        self.drop_frame.config(highlightbackground="#888", highlightcolor="#888")
        self.drop_frame.pack(pady=20)

        # Cloud image (encapsulation of image handling)
        self.load_cloud_image()

        # Instruction label
        self.instruction_label = tk.Label(self.drop_frame, text="Drag and drop your files here", bg="#444", fg="#fff")
        self.instruction_label.pack(pady=10)

        # Browse button
        self.browse_button = tk.Button(self.drop_frame, text="Browse Image", command=self.upload_and_age_image, bg="#444", fg="#fff")
        self.browse_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self, text="No image processed yet.", bg="#2e2e2e", fg="#fff")
        self.status_label.pack(pady=10)

        # Image label (polymorphism: used for different images)
        self.image_label = tk.Label(self, bg="#2e2e2e")
        self.image_label.pack(pady=20)

        # Progress bar (encapsulation: wraps up the progress indicator)
        self.progress_bar = ttk.Progressbar(self, mode="indeterminate", style="dark.Horizontal.TProgressbar")
        self.progress_bar.pack_forget()  # Initially hidden

        # Progress bar styling (Encapsulation)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("dark.Horizontal.TProgressbar", troughcolor='#444', background='#555', thickness=10)

    def load_cloud_image(self): #Encapsulation: Load and display the cloud image
        cloud_image_path = "upload_symbol.png"  # Path to the cloud image
        cloud_img = Image.open(cloud_image_path)
        cloud_img = cloud_img.resize((80, 80))
        cloud_img_tk = ImageTk.PhotoImage(cloud_img)
        cloud_label = tk.Label(self.drop_frame, image=cloud_img_tk, bg="#444")
        cloud_label.image = cloud_img_tk  # Keep a reference to avoid garbage collection
        cloud_label.pack(pady=10)

    def setup_drag_and_drop(self): #Method overriding: Set up drag-and-drop functionality
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.drop_event_handler)

    def drop_event_handler(self, event): #Polymorphism: Handle dropped image files differently based on type
        file_path = event.data
        if file_path.endswith(('.png', '.jpg', '.jpeg')):
            self.start_aging_process(file_path)
        else:
            self.status_label.config(text="Invalid file format. Please drop a PNG or JPEG image.")

    def upload_and_age_image(self): #Encapsulation: Hide the complexity of file dialogs and aging process
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ".png .jpg .jpeg")])
        if file_path:
            self.start_aging_process(file_path)

    def start_aging_process(self, file_path): #Encapsulation: Starts the image aging process
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()

        # Use threading to run the aging process in the background
        threading.Thread(target=self.apply_aging_fast_aging_gan, args=(file_path,)).start()
    
    def apply_aging_fast_aging_gan(self, file_path): #Encapsulation and polymorphism: Applies the aging process using Fast-AgingGAN
        script_path = os.path.join(os.path.dirname(__file__), 'infer.py')

        if not os.path.exists(script_path):
            self.status_label.config(text=f"Error: infer.py not found at {script_path}")
            return

        self.status_label.config(text="Processing image...")
        os.system(f"python \"{script_path}\" --image_path \"{file_path}\"")

        aged_img_path = 'aged_output.png'
        if os.path.exists(aged_img_path):
            # Display the aged image
            aged_img = Image.open(aged_img_path)
            aged_img = aged_img.resize((600, 350))
            img_tk = ImageTk.PhotoImage(aged_img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Avoid garbage collection

            self.status_label.config(text="Processing done, here's your aged look!")
        else:
            self.status_label.config(text="Failed to generate aged image.")

        self.progress_bar.stop()

# Main app execution
if __name__ == "__main__":
    app = FaceAgingApp()  # Create an instance of the app (polymorphism: different app behavior depending on usage)
    app.mainloop()  # Start the event loop (encapsulation: tkinter manages event handling)

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
from cryptography.fernet import Fernet
from ttkthemes import ThemedTk
from tkinter import ttk

# Set up the main application window
root = ThemedTk(theme="radiance")
root.title("Image Encryption/Decryption")
root.geometry("1100x500")
root.resizable(False, False)  # Disable window resizing

# Create a frame for displaying the images
frame = ttk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Labels to display images
original_image_label = ttk.Label(frame, text="Original Image")
original_image_label.grid(row=0, column=0)
encrypted_image_label = ttk.Label(frame, text="Encrypted Image")
encrypted_image_label.grid(row=0, column=1)
decrypted_image_label = ttk.Label(frame, text="Decrypted Image")
decrypted_image_label.grid(row=0, column=2)

# Configure column widths to center the text
for col in range(3):
    frame.grid_columnconfigure(col, weight=1)

# Canvas to show images
original_image_canvas = tk.Canvas(frame, width=300, height=300)
original_image_canvas.grid(row=1, column=0)
encrypted_image_canvas = tk.Canvas(frame, width=300, height=300)
encrypted_image_canvas.grid(row=1, column=1)
decrypted_image_canvas = tk.Canvas(frame, width=300, height=300)
decrypted_image_canvas.grid(row=1, column=2)


# Function to load an image
def load_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if file_path:
        try:
            image = Image.open(file_path)
            img = ImageTk.PhotoImage(image)
            original_image_canvas.create_image(150, 150, image=img)
            original_image_canvas.image = img
            # Save image data for encryption
            image_bytes = io.BytesIO()
            image.save(image_bytes, format=image.format)
            global original_image_data
            original_image_data = image_bytes.getvalue()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")


# Function to generate and save a key
def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)


# Generate the key if it does not exist
try:
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    generate_key()
    with open("encryption_key.key", "rb") as key_file:
        key = key_file.read()

fernet = Fernet(key)
original_image_data = None


# Function to encrypt the image
def encrypt_image():
    if original_image_data:
        encrypted_data = fernet.encrypt(original_image_data)
        save_path = filedialog.asksaveasfilename(
            defaultextension=".enc", filetypes=[("Encrypted files", "*.enc")]
        )
        if save_path:
            with open(save_path, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
            # Display encrypted image placeholder
            encrypted_image_canvas.create_text(150, 150, text="Encrypted", fill="black")
            messagebox.showinfo(
                "Success", f"Image encrypted and saved as '{save_path}'"
            )


# Function to decrypt the image
def decrypt_image():
    file_path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
    if file_path:
        try:
            with open(file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            image_bytes = io.BytesIO(decrypted_data)
            image = Image.open(image_bytes)
            img = ImageTk.PhotoImage(image)
            decrypted_image_canvas.create_image(150, 150, image=img)
            decrypted_image_canvas.image = img

            # Ask the user where to save the decrypted image
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*"),
                ],
            )
            if save_path:
                image.save(save_path)
                messagebox.showinfo(
                    "Success", f"Image decrypted and saved as '{save_path}'"
                )
            else:
                messagebox.showinfo("Success", "Image decrypted and displayed")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# Frame to hold the buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Buttons to load, encrypt, and decrypt images
load_button = ttk.Button(button_frame, text="Load Image", command=load_image)
load_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)
encrypt_button = ttk.Button(button_frame, text="Encrypt Image", command=encrypt_image)
encrypt_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)
decrypt_button = ttk.Button(button_frame, text="Decrypt Image", command=decrypt_image)
decrypt_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)

root.mainloop()

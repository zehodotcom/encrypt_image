import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
from cryptography.fernet import Fernet

# Set up the main application window
root = tk.Tk()
root.title("Image Encryption/Decryption")

# Create a frame for displaying the images
frame = tk.Frame(root)
frame.pack()

# Labels to display images
original_image_label = tk.Label(frame, text="Original Image")
original_image_label.grid(row=0, column=0)
encrypted_image_label = tk.Label(frame, text="Encrypted Image")
encrypted_image_label.grid(row=0, column=1)
decrypted_image_label = tk.Label(frame, text="Decrypted Image")
decrypted_image_label.grid(row=0, column=2)

# Canvas to show images
original_image_canvas = tk.Canvas(frame, width=300, height=300)
original_image_canvas.grid(row=1, column=0)
encrypted_image_canvas = tk.Canvas(frame, width=300, height=300)
encrypted_image_canvas.grid(row=1, column=1)
decrypted_image_canvas = tk.Canvas(frame, width=300, height=300)
decrypted_image_canvas.grid(row=1, column=2)


# Function to load an image
def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        img = ImageTk.PhotoImage(image)
        original_image_canvas.create_image(150, 150, image=img)
        original_image_canvas.image = img
        # Save image data for encryption
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        global original_image_data
        original_image_data = image_bytes.getvalue()


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
        with open("encrypted_image.enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        # Display encrypted image placeholder
        encrypted_image_canvas.create_text(150, 150, text="Encrypted", fill="black")
        messagebox.showinfo(
            "Success", "Image encrypted and saved as 'encrypted_image.enc'"
        )


# Function to decrypt the image
def decrypt_image():
    try:
        with open("encrypted_image.enc", "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        image_bytes = io.BytesIO(decrypted_data)
        image = Image.open(image_bytes)
        image.thumbnail((300, 300))
        img = ImageTk.PhotoImage(image)
        decrypted_image_canvas.create_image(150, 150, image=img)
        decrypted_image_canvas.image = img
        messagebox.showinfo("Success", "Image decrypted and displayed")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Buttons to load, encrypt, and decrypt images
load_button = tk.Button(root, text="Load Image", command=load_image)
load_button.pack(side=tk.LEFT)
encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.pack(side=tk.LEFT)
decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.pack(side=tk.LEFT)

root.mainloop()

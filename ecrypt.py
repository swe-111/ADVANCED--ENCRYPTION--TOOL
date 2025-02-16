import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext
from cryptography.fernet import Fernet

# Function to generate a new encryption key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a single file
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        file_data = file.read()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file_data)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)

# Function to decrypt a single file
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path[:-10], 'wb') as file:  # Remove '.encrypted' from filename
        file.write(decrypted_data)

# Function to select files for encryption
def select_files_to_encrypt():
    file_paths = filedialog.askopenfilenames(title="Select Files to Encrypt", filetypes=[("All Files", "*.*")])
    if file_paths:
        key = generate_key()
        for file_path in file_paths:
            encrypt_file(file_path, key)
        messagebox.showinfo("Success", f"Files encrypted successfully!\nKey: {key.decode()}\nStore this key securely.")

# Function to select files for decryption
def select_files_to_decrypt():
    file_paths = filedialog.askopenfilenames(title="Select Files to Decrypt", filetypes=[("Encrypted Files", "*.encrypted")])
    if file_paths:
        key = simpledialog.askstring("Input", "Enter the encryption key:")
        if key:
            for file_path in file_paths:
                try:
                    decrypt_file(file_path, key.encode())
                except Exception as e:
                    messagebox.showerror("Error", f"Decryption failed for {file_path}: {str(e)}")
            messagebox.showinfo("Success", "Files decrypted successfully!")

# Function to display help information
def show_help():
    help_text = """Advanced Encryption Tool Help:
1. To encrypt files, click 'Encrypt File' and select the files you want to encrypt.
2. A unique encryption key will be generated. Store this key securely, as it is required for decryption.
3. To decrypt files, click 'Decrypt File' and select the encrypted files. Enter the encryption key when prompted.
4. Ensure you have the correct key for decryption, or the process will fail.
"""
    messagebox.showinfo("Help", help_text)

# Create the main application window
app = tk.Tk()
app.title("Advanced Encryption Tool")
app.geometry("400x300")

# Create buttons for encrypting and decrypting files
encrypt_button = tk.Button(app, text="Encrypt Files", command=select_files_to_encrypt)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(app, text="Decrypt Files", command=select_files_to_decrypt)
decrypt_button.pack(pady=10)

help_button = tk.Button(app, text="Help", command=show_help)
help_button.pack(pady=10)

# Run the application
app.mainloop()
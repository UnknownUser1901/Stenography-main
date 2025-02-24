import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import time
import sys
import subprocess
import hashlib

class ImageSteganography:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("5600x1000")
        
        self.image_path = None
        self.stored_password = None
        self.message_length = 0
        
        # Character Mapping
        self.d = {chr(i): i for i in range(255)}
        self.c = {i: chr(i) for i in range(255)}
        
        # GUI Elements
        tk.Label(root, text="Secure Data Using Image Steganography", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Image Selection
        self.image_label = tk.Label(root, text="No image selected")
        self.image_label.pack()
        tk.Button(root, text="Select Image", command=self.select_image).pack(pady=5)
        
        # Image Display
        self.image_display = tk.Label(root)
        self.image_display.pack()
        
        # Encoding Section
        tk.Label(root, text="Enter Message to Encode:").pack(pady=5)
        self.msg_entry = tk.Text(root, height=4, width=40)
        self.msg_entry.pack()
        
        tk.Label(root, text="Enter Password:").pack(pady=5)
        self.pass_entry = tk.Entry(root, show="*")
        self.pass_entry.pack()
        
        tk.Button(root, text="Encode",fg="red", command=self.encode).pack(pady=5)
        
        # Decoding Section
        tk.Button(root, text="Decode Message",fg="green",command=self.decode).pack(pady=5)
        tk.Label(root, text="Decrypted Message:").pack(pady=5)
        self.decrypted_msg = tk.Text(root, height=4, width=40, state='disabled')
        self.decrypted_msg.pack()
        
        # Status Label
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)
        
    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if self.image_path:
            self.image_label.config(text=os.path.basename(self.image_path))
            img = Image.open(self.image_path)
            img = img.resize((300, 300))
            img = ImageTk.PhotoImage(img)
            self.image_display.config(image=img)
            self.image_display.image = img
            
            # Reset decrypted message field
            self.decrypted_msg.config(state='normal')
            self.decrypted_msg.delete("1.0", tk.END)
            self.decrypted_msg.config(state='disabled')
            self.result_label.config(text="")
            
            # Only show hash if it's an encrypted image
            filename = os.path.basename(self.image_path)
            if filename.startswith("encoded_image_"):
                with open(self.image_path, 'rb') as f:
                    image_hash = hashlib.sha256(f.read()).hexdigest()
                self.msg_entry.delete("1.0", tk.END)  # Reset previous content
                self.msg_entry.insert("1.0", image_hash)
                print(f"Encrypted image hash: {image_hash}")  # Debug output
            else:
                # Clear message field for normal images if it contains a hash
                current_text = self.msg_entry.get("1.0", tk.END).strip()
                if current_text and len(current_text) == 64 and all(c in "0123456789abcdef" for c in current_text):
                    self.msg_entry.delete("1.0", tk.END)
                print(f"Selected normal image: {filename}")  # Debug output
    
    def encode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image")
            return

        msg = self.msg_entry.get("1.0", tk.END).strip()
        password = self.pass_entry.get()

        if not msg or not password:
            messagebox.showerror("Error", "Please enter both message and password")
            return

        # Generate SHA-256 hash of the message (for display only)
        msg_hash = hashlib.sha256(msg.encode()).hexdigest()
        print(f"Encoding message: {msg}")  # Debug output
        
        img = cv2.imread(self.image_path)
        if img is None:
            messagebox.showerror("Error", "Invalid image file")
            return

        # Check if the original message fits in the image
        if (len(msg) + 4) * 3 > img.shape[0] * img.shape[1]:
            messagebox.showerror("Error", "Message too large for image")
            return
        
        # Encode message length and original message
        self.message_length = len(msg)
        n, m, z = 0, 0, 0
        
        length_bytes = self.message_length.to_bytes(4, byteorder='big')
        for byte in length_bytes:
            img[n, m, z] = byte
            n += 1
            m += 1
            z = (z + 1) % 3

        for char in msg:
            img[n, m, z] = self.d[char]
            n += 1
            m += 1
            z = (z + 1) % 3

        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_filename = f"encoded_image_{timestamp}.png"
        output_path = os.path.join(os.getcwd(), output_filename)

        cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        
        # Reset all fields except message field, which shows hash
        self.image_path = None
        self.image_label.config(text="No image selected")
        self.image_display.config(image='')
        self.image_display.image = None
        self.pass_entry.delete(0, tk.END)
        self.decrypted_msg.config(state='normal')
        self.decrypted_msg.delete("1.0", tk.END)
        self.decrypted_msg.config(state='disabled')
        self.result_label.config(text="")
        
        self.msg_entry.delete("1.0", tk.END)
        self.msg_entry.insert("1.0", msg_hash)
        
        messagebox.showinfo("Success", f"Message encoded successfully!\nSaved as {output_filename}")
        
        try:
            if os.name == 'nt':
                os.startfile(output_path)
            elif os.name == 'posix':
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, output_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open the image: {e}")

        self.stored_password = password
        
    def decode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image")
            return
        
        password = self.pass_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter password")
            return
        
        if not hasattr(self, 'stored_password') or password != self.stored_password:
            messagebox.showerror("Error", "Incorrect password")
            return
        
        img = cv2.imread(self.image_path)
        if img is None:
            messagebox.showerror("Error", "Invalid image file")
            return
        
        try:
            n, m, z = 0, 0, 0
            length_bytes = bytearray()
            for _ in range(4):
                length_bytes.append(img[n, m, z])
                n += 1
                m += 1
                z = (z + 1) % 3
            
            msg_length = int.from_bytes(length_bytes, byteorder='big')
            print(f"Decoded message length: {msg_length}")  # Debug output
            
            message = ""
            for _ in range(msg_length):
                if n >= img.shape[0] or m >= img.shape[1]:
                    print(f"Stopped at n={n}, m={m}, z={z} due to image bounds")
                    break
                char_val = img[n, m, z]
                message += self.c[char_val]
                n += 1
                m += 1
                z = (z + 1) % 3
            
            print(f"Decoded message: {message}")  # Debug output
            
            self.decrypted_msg.config(state='normal')
            self.decrypted_msg.delete("1.0", tk.END)
            if not message:
                self.decrypted_msg.insert("1.0", "No message found or empty message")
                self.result_label.config(text="Decoding completed - No message found")
            else:
                self.decrypted_msg.insert("1.0", message)
                self.result_label.config(text="Message decoded successfully")
            self.decrypted_msg.config(state='disabled')
            
        except Exception as e:
            print(f"Decoding error: {e}")  # Debug output
            messagebox.showerror("Error", f"Failed to decode message: {e}")
            self.decrypted_msg.config(state='normal')
            self.decrypted_msg.delete("1.0", tk.END)
            self.decrypted_msg.insert("1.0", "Error decoding message")
            self.decrypted_msg.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageSteganography(root)
    root.mainloop()

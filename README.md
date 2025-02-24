# Stenography-main
Secure Data Hiding in Images using Steganography

## Overview
This project implements **Image Steganography** using Python, allowing users to securely hide and retrieve messages within images. It ensures safe communication by embedding text inside image pixels without noticeable alterations.

## Features
✅ **Hide messages inside images** (Steganography)  
✅ **Password-protected encoding & decoding**  
✅ **Graphical User Interface (GUI) using Tkinter**  
✅ **Detects encrypted images automatically**  
✅ **Displays image hash for integrity verification**  

## Technologies Used
- **Programming Language:** Python
- **GUI:** Tkinter
- **Libraries:** OpenCV, PIL (Pillow), hashlib
- **Hashing:** SHA-256 for password security

## Installation
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-username/Image-Steganography.git
   cd Image-Steganography
   ```
2. **Install Required Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Running the Application
Execute the Python script:
```sh
python stegonew.py
```

### Encoding a Message
1. Select an image using the **"Select Image"** button.
2. Enter the **message** you want to hide.
3. Set a **password** for protection.
4. Click **"Encode"** to hide the message inside the image.

### Decoding a Message
1. Select the **encoded image**.
2. Enter the correct **password**.
3. Click **"Decode Message"** to retrieve the hidden text.

## Screenshots
![Encoding](Screenshot(6).png)  
![Decoding](Screenshot(7).png)  
![Application Interface](Screenshot(8).png)  

## Future Enhancements
🚀 Implement **AES encryption** for stronger security  
🚀 Extend support to **video steganography**  
🚀 Improve UI for a better user experience  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

## License
This project is licensed under the **MIT License**.

## Contact
🔗 **GitHub:** https://github.com/UnknownUser1901 
📧 **Email:** mukulchoudhary1901@Gmail.com


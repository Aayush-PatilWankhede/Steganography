import cv2
import numpy as np

def decrypt_image(password):
    print("Starting decryption...")  # Debugging
    img = cv2.imread("encrypted_image.png")  # Load PNG instead of JPG
    
    if img is None:
        print("Error: Encrypted image not found! Make sure 'encrypted_image.png' exists.")
        return
    
    print("Image successfully loaded.")  # Debugging
    binary_message = ""
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                binary_message += str(img[i, j, k] & 1)
    
    if not binary_message:
        print("Error: No binary data extracted. The image may not contain a message.")
        return
    
    try:
        chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
        extracted_message = ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
        
        if len(extracted_message) < 3:
            print("Error: Extracted message too short, possibly corrupted.")
            return
        
        message_length = int(extracted_message[:3])
        stored_password = extracted_message[3:3+len(password)]
        secret_message = extracted_message[3+len(password):3+len(password)+message_length]
        
        if password == stored_password:
            print("Decrypted Message:", secret_message)
        else:
            print("Incorrect password! Decryption failed.")
    except Exception as e:
        print("Error during decryption:", str(e))
        print("Decryption failed. Make sure the correct image and password are used.")

if __name__ == "__main__":
    passcode = input("Enter passcode for decryption: ")
    decrypt_image(passcode)

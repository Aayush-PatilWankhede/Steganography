import cv2
import os
import numpy as np

def encrypt_image(message, password):
    img = cv2.imread("image.jpg")
    if img is None:
        print("Error: Image not found!")
        return
    
    message = f"{len(message):03d}" + password + message  # Store length + password
    required_bits = len(message) * 8
    available_bits = img.shape[0] * img.shape[1] * 3
    
    if required_bits > available_bits:
        print("Error: Message too long to hide in image.")
        return
    
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    idx = 0
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(3):
                if idx < len(binary_message):
                    img[i, j, k] = (img[i, j, k] & 254) | int(binary_message[idx])
                    idx += 1
                else:
                    break
    
    cv2.imwrite("encrypted_image.png", img)  # Save as PNG to prevent compression artifacts
    print("Encryption successful! Image saved as encrypted_image.png")
    os.system("start encrypted_image.png")

if __name__ == "__main__":
    secret_msg = input("Enter secret message: ")
    passcode = input("Enter a passcode: ")
    encrypt_image(secret_msg, passcode)
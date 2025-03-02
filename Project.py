import cv2
import os

# Load the image
img = cv2.imread("image.jpg")  # Replace with the correct image path
if img is None:
    print("Error: Image not found. Check the file path.")
    exit()

# Input secret message and passcode
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Character to ASCII mappings
d = {chr(i): i for i in range(255)}
c = {i: chr(i) for i in range(255)}

# Get image dimensions
height, width, _ = img.shape
max_capacity = height * width * 3  # Maximum bytes we can store

# Ensure message fits in the image
if len(msg) + 4 > max_capacity:  # +4 bytes to store message length
    print("Error: Message too long for the image size.")
    exit()

# Convert message length to 4 bytes and store it first
msg_length = len(msg)
length_bytes = [(msg_length >> (i * 8)) & 0xFF for i in range(4)]

# Encode message length
n, m, z = 0, 0, 0
for byte in length_bytes:
    img[n, m, z] = byte
    n, m, z = n + 1, m + 1, (z + 1) % 3

# Encode the message
for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    n, m, z = n + 1, m + 1, (z + 1) % 3

# Save and open the encrypted image
cv2.imwrite("encryptedImage.jpg", img)
if os.name == "nt":  # Windows
    os.system("start encryptedImage.jpg")
else:  # Linux/Mac
    os.system("xdg-open encryptedImage.jpg" if os.name == "posix" else "open encryptedImage.jpg")

# Decryption
message = ""
n, m, z = 0, 0, 0

# Ask for the passcode
pas = input("Enter passcode for Decryption: ")
if password == pas:
    # Retrieve message length
    msg_length = sum(img[n + i, m + i, (z + i) % 3] << (i * 8) for i in range(4))
    n, m, z = 4, 4, 1  # Move past the length bytes

    # Retrieve the message
    for i in range(msg_length):
        message += c[img[n, m, z]]
        n, m, z = n + 1, m + 1, (z + 1) % 3

    print("Decryption message:", message)
else:
    print("YOU ARE NOT AUTHORIZED")

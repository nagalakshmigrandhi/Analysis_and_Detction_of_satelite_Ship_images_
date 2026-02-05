import cv2
import numpy as np
import requests
from PIL import Image
from io import BytesIO
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
import os

def process_image(image_path):
    """
    Process the image (either local path or URL) and return the processed image
    """
    try:
        # Try to open as URL first
        try:
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        except requests.exceptions.RequestException:
            # If URL fails, try as local file
            image = Image.open(image_path)
        
        # Convert to OpenCV format
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale easier to process
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur for reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply Canny for edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Detects object outlines from the edges. 
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw contours on the original image to green image
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
        
        return image
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        process_and_show_image(file_path)

def process_url():
    url = url_entry.get()
    if url:
        process_and_show_image(url)
    else:
        messagebox.showwarning("Input Error", "Please enter a URL")

def process_and_show_image(image_path):
    result = process_image(image_path)
    if result is not None:
        cv2.imshow('Detected Ships', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        messagebox.showerror("Error", "Failed to process the image")

def create_gui():
    root = Tk()
    root.title("Ship Detection System")
    root.geometry("400x200")
    
    # URL input section
    url_label = Label(root, text="Enter Image URL:")
    url_label.pack(pady=5)
    
    global url_entry
    url_entry = Entry(root, width=50)
    url_entry.pack(pady=5)
    
    # URL button
    url_button = Button(root, text="Process URL", command=process_url)
    url_button.pack(pady=5)
    
    # Upload button
    upload_button = Button(root, text="Upload Image", command=upload_image)
    upload_button.pack(pady=5)
    
    # Exit button
    exit_button = Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()

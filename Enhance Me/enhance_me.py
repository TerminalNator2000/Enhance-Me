import PySimpleGUI as sg
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os
import io

# Define constants for the GUI layout and functionality
WINDOW_TITLE = "Enhance Me - Image Editing GUI"
DEFAULT_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp"]
WINDOW_SIZE = (800, 600)
IMAGE_DISPLAY_SIZE = (600, 400)

# Function to load an image and resize it to fit the window
def load_image(file_path):
    image = Image.open(file_path)
    image.thumbnail(IMAGE_DISPLAY_SIZE, Image.LANCZOS)
    return image

# Function to display an image in PySimpleGUI
def display_image(window, image_pil, element_key):
    image_bytes = io.BytesIO()
    image_pil.save(image_bytes, format="PNG")
    window[element_key].update(data=image_bytes.getvalue())

# Function to handle erasing artifacts from the image
def erase_at_point(np_image, x, y, radius=10):
    """ Erase at the given point (x, y) with a specified radius """
    h, w, _ = np_image.shape
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (x, y), radius, 255, -1)
    np_image[mask == 255] = [255, 255, 255]  # Replace with white color for visibility
    return np_image

# Main GUI layout with scroll bars
layout = [
    [sg.Text("Choose an Image File:"), sg.Input(), sg.FileBrowse(key="-FILE-"), sg.Button("Load Image"), sg.Button("Rollback")],
    [
        sg.Column(
            layout=[[sg.Image(key="-IMAGE-", expand_x=True, expand_y=True)]],
            size=(None, None),
            scrollable=True,
            vertical_scroll_only=False,
            key="-IMAGE_COLUMN-",
            expand_x=True,
            expand_y=True
        )
    ],
    [
        sg.Button("Zoom In"), sg.Button("Zoom Out"),
        sg.Button("Sharpen +"), sg.Button("Sharpen -"),
        sg.Button("Erase Artifacts"),
        sg.Button("Add Artifacts"),
        sg.Button("Add Text"),
        sg.Button("Add Borders"),
        sg.Button("Cartoonize"),
    ],
    [sg.Text("Save as:")],
    [sg.Input(default_text="enhanced_image"), sg.Combo(DEFAULT_IMAGE_FORMATS, key="-FORMAT-", default_value="jpg"), sg.Button("Save Image")],
]

# Create a window instance
window = sg.Window(WINDOW_TITLE, layout, size=WINDOW_SIZE, resizable=True, finalize=True, element_justification='center')

# Initialize an empty variable for the current loaded image
current_image = None
image_history = []

# Event loop to handle user interaction
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    # Handle loading the image
    elif event == "Load Image":
        file_path = values["-FILE-"]
        if os.path.exists(file_path):
            current_image = load_image(file_path)
            image_history = [current_image.copy()]
            display_image(window, current_image, "-IMAGE-")
        else:
            sg.popup_error("Error: File not found!")

    # Handle zoom in
    elif event == "Zoom In" and current_image:
        width, height = current_image.size
        image_history.append(current_image.copy())
        current_image = current_image.resize((int(width * 1.25), int(height * 1.25)), Image.LANCZOS)
        display_image(window, current_image, "-IMAGE-")

    # Handle zoom out
    elif event == "Zoom Out" and current_image:
        width, height = current_image.size
        image_history.append(current_image.copy())
        current_image = current_image.resize((int(width * 0.8), int(height * 0.8)), Image.LANCZOS)
        display_image(window, current_image, "-IMAGE-")

    # Handle sharpen with buttons
    elif event == "Sharpen +" and current_image:
        image_history.append(current_image.copy())
        enhancer = ImageEnhance.Sharpness(current_image)
        current_image = enhancer.enhance(2.0)
        display_image(window, current_image, "-IMAGE-")
    elif event == "Sharpen -" and current_image:
        image_history.append(current_image.copy())
        enhancer = ImageEnhance.Sharpness(current_image)
        current_image = enhancer.enhance(0.5)
        display_image(window, current_image, "-IMAGE-")

    # Handle erase artifacts with click interaction
    elif event == "Erase Artifacts" and current_image:
        sg.popup("Click on the artifact you want to erase.")
        np_image = np.array(current_image)
        while True:
            click_event, click_values = window.read()
            if click_event == sg.WIN_CLOSED or click_event == "Cancel":
                break
            elif isinstance(click_event, tuple):
                try:
                    x, y = click_event
                    if x is not None and y is not None:
                        # Adjust the coordinates based on the image scale
                        image_width, image_height = current_image.size
                        display_element = window["-IMAGE-"]
                        element_width, element_height = display_element.get_size()
                        scale_x = image_width / element_width
                        scale_y = image_height / element_height
                        adjusted_x = int(x * scale_x)
                        adjusted_y = int(y * scale_y)

                        # Erase artifact at the clicked position
                        image_history.append(current_image.copy())
                        np_image = erase_at_point(np_image, adjusted_x, adjusted_y, radius=10)
                        current_image = Image.fromarray(np_image)
                        display_image(window, current_image, "-IMAGE-")
                        break
                except Exception as e:
                    sg.popup_error(f"Unable to get click coordinates: {e}")

    # Handle add artifacts
    elif event == "Add Artifacts" and current_image:
        # Example: Add noise (placeholder for adding artifacts)
        np_image = np.array(current_image)
        noise = np.random.randint(0, 50, (np_image.shape[0], np_image.shape[1], 3), dtype='uint8')
        np_image = np.clip(np_image + noise, 0, 255)
        image_history.append(current_image.copy())
        current_image = Image.fromarray(np_image)
        display_image(window, current_image, "-IMAGE-")

    # Handle add text
    elif event == "Add Text" and current_image:
        text = sg.popup_get_text("Enter text to add:")
        if text:
            np_image = np.array(current_image)
            cv2.putText(np_image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            image_history.append(current_image.copy())
            current_image = Image.fromarray(np_image)
            display_image(window, current_image, "-IMAGE-")

    # Handle add borders
    elif event == "Add Borders" and current_image:
        border_size = sg.popup_get_text("Enter border size in pixels:")
        if border_size.isdigit():
            border_size = int(border_size)
            image_history.append(current_image.copy())
            current_image = ImageOps.expand(current_image, border=border_size, fill='black')
            display_image(window, current_image, "-IMAGE-")

    # Handle cartoonize
    elif event == "Cartoonize" and current_image:
        np_image = np.array(current_image)
        gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 10)
        color = cv2.bilateralFilter(np_image, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        current_image = Image.fromarray(cartoon)
        display_image(window, current_image, "-IMAGE-")

    # Handle save image
    elif event == "Rollback" and current_image and image_history:
        current_image = image_history.pop()
        display_image(window, current_image, "-IMAGE-")
    elif event == "Save Image" and current_image:
        output_file_name = values[0]
        output_format = values["-FORMAT-"]
        if output_format.lower() in DEFAULT_IMAGE_FORMATS:
            current_image.save(f"{output_file_name}.{output_format}", output_format.upper())
            sg.popup_ok("Image saved successfully!")

# Close the window
window.close()












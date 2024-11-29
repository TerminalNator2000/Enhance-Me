# Enhance Me - Image Editing GUI

## Overview
Enhance Me is a graphical user interface (GUI) application built with Python using `PySimpleGUI`, `OpenCV`, and `Pillow`. The application allows users to load, edit, and save images using various tools such as sharpening, zooming, artifact erasing, adding text, borders, and even applying a cartoon effect.

## Features
- **Load Image**: Open an image file to begin editing.
- **Zoom In/Out**: Incrementally zoom in or out on the loaded image.
- **Sharpen/Soften**: Adjust the sharpness of the image.
- **Erase Artifacts**: Click to remove unwanted artifacts in the image.
- **Add Artifacts**: Randomly add noise to the image to create artifacts.
- **Add Text**: Add customizable text to the image.
- **Add Borders**: Add a colored border around the image.
- **Cartoonize**: Apply a cartoon-like filter to the image.
- **Save Image**: Save the edited image in various formats (e.g., JPG, PNG, WEBP).
- **Rollback**: Revert back to the previous version of the image.

## Installation

To run this project locally, you need to have Python 3 installed. You'll also need to install some required dependencies.

### Dependencies
- Python 3.x
- `PySimpleGUI`
- `opencv-python`
- `numpy`
- `Pillow`

You can install the required packages using the following command:
```bash
pip install PySimpleGUI opencv-python numpy Pillow
```

## How to Use
1. **Launch the Application**: Run the `enhance_me.py` script.
   ```bash
   python enhance_me.py
   ```
2. **Load an Image**: Click on "Browse" to select an image file and load it into the application.
3. **Edit the Image**: Use the various buttons to edit the image:
   - **Zoom In/Out**: Click "Zoom In" or "Zoom Out" to adjust the image size.
   - **Sharpen + / -**: Increase or decrease the sharpness of the image.
   - **Erase Artifacts**: Click on the image area where you want to remove artifacts.
   - **Add Text**: Click "Add Text" and enter the desired text to overlay on the image.
   - **Add Borders**: Click "Add Borders" and specify the border size in pixels.
   - **Cartoonize**: Apply a cartoon effect to your image.
4. **Save the Image**: Specify a file name and format, then click "Save Image".
5. **Rollback**: If you make a mistake, click "Rollback" to undo the last action.

## Known Issues
- The **Erase Artifacts** function may not work as expected for complex images or high-resolution images. Future improvements will be made to refine this functionality.
- Scrollbars for zoomed images may sometimes behave inconsistently, depending on image size.

## Future Improvements
- Add advanced artifact removal using AI-based inpainting techniques.
- Improve the scrollability of the interface when zooming in and out.
- Implement more advanced filters, including color corrections and effects.
- Support for batch image processing.

## Contributing
Contributions are welcome! If you'd like to improve this project, please feel free to submit a pull request or create an issue on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- **PySimpleGUI**: For providing a simple way to create GUI applications in Python.
- **OpenCV**: For image processing capabilities.
- **Pillow**: For easy image manipulation.

## Contact
If you have any questions or suggestions, please contact me at `mnations058@gmail.com`.


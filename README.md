# File-Converter

File-Converter is a Python-based web application designed to provide users with the ability to convert files between different formats. This project was deployed using Render and demonstrates how simple it can be to create and host a web application for file conversions.

## Features
- **PDF to Image Converter**: Converts PDF files to image formats (JPG or PNG).
- **Image to PDF Converter**: Merges multiple image files into a single PDF.
- **PDF to DOCX Converter**: Converts PDF files to editable Word documents.
- **HEIC to PNG Converter**: Converts HEIC image files to PNG format.

## Live Demo
You can try the live version of the app here: [File-Converter](https://file-converter-ljqd.onrender.com/).

## Tools and Technologies Used
### **Backend**
- **Python**: The core programming language for building the application.
- **Flask**: A lightweight web framework for handling routes and requests.
- **Gunicorn**: A WSGI server for serving the Flask application in a production environment.

### **File Processing Libraries**
- **pdf2image**: For converting PDF files into images.
- **Pillow (PIL)**: For image processing and merging images into PDFs.
- **pdfminer.six**: For extracting text from PDF files to facilitate PDF-to-DOCX conversion.
- **python-docx**: For creating Word documents programmatically.
- **pillow-heif**: For handling HEIC files and converting them to PNG.

### **Deployment**
- **Render**: A modern cloud platform used for deploying the application. Render handles the environment setup and provides a live URL for public access.

### **Other Tools**
- **pip**: For managing and installing Python dependencies.
- **Git**: For version control and pushing code to the repository.
- **Procfile**: For specifying the commands needed to run the app on Render.

## How It Works
1. **Upload Files**: Users can upload files (PDFs, images) via the intuitive web interface.
2. **Select Options**: Choose the desired conversion type (e.g., PDF to Image, Image to PDF).
3. **Download Results**: The converted files are automatically downloaded to the user’s system.

## Folder Structure
File-Converter/ ├── File-Converter.py # Main application file ├── requirements.txt # List of dependencies ├── runtime.txt # Specifies the Python version ├── render.yaml # Configuration file for Render deployment ├── Procfile # Specifies the app's start command ├── README.md # Project documentation └── static/ # Folder for static assets (if any)


## Deployment
This app was deployed using Render, a platform that simplifies hosting web applications. The deployment process involved:
1. Writing a `render.yaml` file to specify system dependencies (like `poppler-utils`) and Python dependencies.
2. Adding necessary Python packages to the `requirements.txt` file.
3. Configuring the `startCommand` to run the app using `gunicorn`.

If you're looking to host your own projects, Render is a great platform for beginners and professionals alike.

## Challenges and Learnings
This was my first experience deploying an app, and while there were initial challenges (e.g., configuring dependencies and deployment settings), I learned a lot about Python packaging, server environments, and deployment pipelines. Special thanks to OpenAI's ChatGPT for the helpful guidance during the process.

## Future Enhancements
- Add support for more file conversion types (e.g., DOCX to PDF).
- Optimize performance for large files.
- Implement user authentication for personalized file storage.

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests with enhancements or bug fixes.

## License
This project is open-source and available under the MIT License.

## Acknowledgments
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Render Documentation](https://render.com/docs)
- [ChatGPT](https://openai.com/chatgpt) for deployment guidance.
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [pillow-heif Documentation](https://pillow-heif.readthedocs.io/)


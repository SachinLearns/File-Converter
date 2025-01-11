from flask import Flask, render_template_string, request, send_file, make_response
from werkzeug.utils import secure_filename
import os
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
from pdfminer.high_level import extract_text
from docx import Document
import pillow_heif

app = Flask(__name__)

# Set up the maximum file size (10 MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTML template for the interface
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Converter</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #333;
        }}
        header {{
            background-color: #4CAF50;
            color: white;
            padding: 1rem 0;
            text-align: center;
        }}
        main {{
            padding: 2rem;
            max-width: 800px;
            margin: auto;
            background: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }}
        h1, h2 {{
            color: #333;
        }}
        form {{
            margin-bottom: 2rem;
            padding: 1rem;
            border: 1px solid #ccc;
            border-radius: 8px;
            background: #f9f9f9;
        }}
        label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }}
        input[type="file"], button {{
            margin-top: 0.5rem;
            padding: 0.5rem;
            font-size: 1rem;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 100%;
        }}
        button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        footer {{
            margin-top: 2rem;
            text-align: center;
            padding: 1rem;
            background-color: #4CAF50;
            color: white;
        }}
    </style>
</head>
<body>
    <header>
        <h1>File Converter</h1>
    </header>
    <main>

        <h2>HEIC to PNG Converter</h2>
        <form action="/upload_heic" method="post" enctype="multipart/form-data">
            <label for="heic">Choose a HEIC file (max 10 MB):</label>
            <input type="file" id="heic" name="heic" accept="image/heic" required>
            <button type="submit">Convert</button>
        </form>

        <h2>PDF to Image Converter</h2>
        <form action="/upload_pdf" method="post" enctype="multipart/form-data">
            <label for="pdf">Choose a PDF file (max 10 MB):</label>
            <input type="file" id="pdf" name="pdf" accept="application/pdf" required>
            <label for="format">Select image format:</label>
            <input type="radio" id="jpg" name="format" value="JPG" checked> JPG
            <input type="radio" id="png" name="format" value="PNG"> PNG
            <button type="submit">Convert</button>
        </form>

        <h2>Image to PDF Converter</h2>
        <form action="/upload_images" method="post" enctype="multipart/form-data">
            <label for="images">Choose image files (max 10 MB each):</label>
            <input type="file" id="images" name="images" accept="image/*" multiple required>
            <button type="submit">Convert</button>
        </form>

        <h2>PDF to DOCX Converter</h2>
        <form action="/upload_pdf_to_docx" method="post" enctype="multipart/form-data">
            <label for="pdf_to_docx">Choose a PDF file (max 10 MB):</label>
            <input type="file" id="pdf_to_docx" name="pdf_to_docx" accept="application/pdf" required>
            <button type="submit">Convert</button>
        </form>
    </main>
    <footer>
        <p>Powered by <a href="https://sachinlearns.com/" target="_blank">SachinLearns</a></p>
    </footer>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload_heic', methods=['POST'])
def upload_heic():
    if 'heic' not in request.files:
        return "No file part", 400

    heic_file = request.files['heic']
    if heic_file.filename == '':
        return "No selected file", 400

    # Save the HEIC file
    filename = secure_filename(heic_file.filename)
    heic_path = os.path.join(UPLOAD_FOLDER, filename)
    heic_file.save(heic_path)

    try:
        # Convert HEIC to PNG using pillow-heif
        pillow_heif.register_heif_opener()  # Register HEIC opener for Pillow
        image = Image.open(heic_path)
        
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        image.save(output_path, "PNG")

        # Prepare response
        response = make_response(send_file(output_path, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename={output_filename}'

        # Clean up
        os.remove(heic_path)

        return response

    except Exception as e:
        if os.path.exists(heic_path):
            os.remove(heic_path)
        return f"Error processing file: {e}", 500


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return "No file part", 400

    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return "No selected file", 400

    # Save the PDF file
    filename = secure_filename(pdf_file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(pdf_path)

    # Get the selected format
    img_format = request.form.get('format', 'JPG')

    # Convert PDF to images
    try:
        images = convert_from_path(pdf_path)
        output_zip = BytesIO()

        with BytesIO() as zip_buffer:
            from zipfile import ZipFile
            with ZipFile(zip_buffer, 'w') as zip_file:
                for i, image in enumerate(images):
                    save_format = 'JPEG' if img_format == 'JPG' else 'PNG'
                    output_filename = f"page_{i + 1}.{img_format.lower()}"
                    with BytesIO() as image_buffer:
                        image.save(image_buffer, format=save_format)
                        image_buffer.seek(0)
                        zip_file.writestr(output_filename, image_buffer.read())

            zip_buffer.seek(0)
            response = make_response(zip_buffer.read())
            response.headers['Content-Type'] = 'application/zip'
            response.headers['Content-Disposition'] = 'attachment; filename=converted_images.zip'

        # Delete the uploaded PDF after use
        os.remove(pdf_path)

        return response

    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return f"Error processing file: {e}", 500

@app.route('/upload_images', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return "No file part", 400

    images = request.files.getlist('images')
    if not images:
        return "No selected files", 400

    try:
        pdf_bytes = BytesIO()
        pil_images = []

        for image_file in images:
            image = Image.open(image_file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            pil_images.append(image)

        if pil_images:
            pil_images[0].save(pdf_bytes, format='PDF', save_all=True, append_images=pil_images[1:])
            pdf_bytes.seek(0)

        response = make_response(pdf_bytes.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=converted_images.pdf'

        return response

    except Exception as e:
        return f"Error processing images: {e}", 500

@app.route('/upload_pdf_to_docx', methods=['POST'])
def upload_pdf_to_docx():
    if 'pdf_to_docx' not in request.files:
        return "No file part", 400

    pdf_file = request.files['pdf_to_docx']
    if pdf_file.filename == '':
        return "No selected file", 400

    # Save the PDF file
    filename = secure_filename(pdf_file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf_file.save(pdf_path)

    # Convert PDF to DOCX
    try:
        text = extract_text(pdf_path)
        doc = Document()
        for line in text.splitlines():
            doc.add_paragraph(line)

        docx_bytes = BytesIO()
        doc.save(docx_bytes)
        docx_bytes.seek(0)

        response = make_response(docx_bytes.read())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        response.headers['Content-Disposition'] = 'attachment; filename=converted_document.docx'

        # Delete the uploaded PDF after use
        os.remove(pdf_path)

        return response

    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        return f"Error processing file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

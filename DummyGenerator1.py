import os
import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import base64

# Configuración del tema (opcional)
st.set_page_config(
    page_title="Generador de Archivos",
    page_icon="📄",
)

# Convierte la imagen a base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# URL de la imagen y enlace a YouTube
logo_path = "Screenshot_46.jpg"
youtube_link = "https://www.youtube.com/@QAtotheSoftware"
logo_base64 = image_to_base64(logo_path)

# Mostrar imagen enlazada
st.markdown(
    f'<a href="{youtube_link}" target="_blank">'
    f'<img src="data:image/jpeg;base64,{logo_base64}" style="width:100%;"/>'
    '</a>',
    unsafe_allow_html=True
)


# Tamaño máximo permitido en MB (1 GB)
MAX_SIZE_MB = 1024  # 1 GB (1024 MB)

# Función para generar un archivo PDF con tamaño específico
def generate_pdf(size_mb):
    # Crear un PDF base en un buffer
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Contenido básico del PDF
    c.drawString(100, 750, "Generado por Maxi Matrero, https://www.youtube.com/@QAtotheSoftware")
    c.save()

    # Obtener el tamaño actual del PDF y calcular el relleno necesario
    pdf_buffer.seek(0)
    pdf_content = pdf_buffer.read()
    target_size = size_mb * 1024 * 1024
    padding_size = target_size - len(pdf_content)

    # Usar un solo bloque de bytes para el relleno
    final_buffer = BytesIO()
    final_buffer.write(pdf_content)
    final_buffer.write(b'\x00' * padding_size)

    return final_buffer.getvalue()

# Función para generar archivos dummy en diferentes formatos con un tamaño específico
def generate_dummy_file(size_mb, file_format):
    if file_format == "PDF":
        return generate_pdf(size_mb)
    else:
        # Encabezados básicos por tipo de archivo
        headers = {
            "TXT": b"",
            "DOCX": b"\x50\x4B\x03\x04",  # DOCX ZIP header
            "RTF": b"{\\rtf1",
            "ODT": b"\x50\x4B\x03\x04",  # ODT ZIP header
            "XLSX": b"\x50\x4B\x03\x04",  # XLSX ZIP header
            "CSV": b"",
            "MP3": b"\x49\x44\x33",
            "WAV": b"RIFF",
            "AAC": b"",
            "FLAC": b"fLaC",
            "OGG": b"OggS",
            "WMA": b"",
            "MP4": b"\x00\x00\x00\x18ftypmp42",
            "AVI": b"RIFF",
            "MKV": b"\x1A\x45\xDF\xA3",
            "MOV": b"moov",
            "WMV": b"",
            "FLV": b"FLV",
            "JPEG": b"\xFF\xD8\xFF",
            "PNG": b"\x89PNG\r\n\x1a\n",
            "GIF": b"GIF89a",
            "BMP": b"BM",
            "TIFF": b"II*\x00",
            "SVG": b"",
            "ZIP": b"PK\x03\x04",
            "RAR": b"Rar!\x1A\x07\x00",
            "7Z": b"7z\xBC\xAF'\x1C",
            "TAR": b"",
            "GZ": b"\x1F\x8B",
            "MDB": b"\x00\x01\x00\x00Standard Jet DB",
            "ACCDB": b"\x00\x01\x00\x00Standard Jet DB",
            "SQL": b"",
            "DBF": b"\x03"
        }
        
        # Obtener el encabezado del tipo de archivo
        file_content = headers.get(file_format, b"")
        
        # Calcular la cantidad de bytes de relleno
        target_size = size_mb * 1024 * 1024
        padding_size = target_size - len(file_content)
        
        # Crear relleno en un solo bloque
        file_content += b'\x00' * padding_size

        return file_content

# Interfaz de Streamlit
st.title("Generador de Archivos Dummy")
file_format = st.selectbox(
    "Selecciona el tipo de archivo",
    ["PDF", "TXT", "DOCX", "RTF", "ODT", "XLSX", "CSV", "MP3", "WAV", "AAC", "FLAC", "OGG", "WMA",
     "MP4", "AVI", "MKV", "MOV", "WMV", "FLV", "JPEG", "PNG", "GIF", "BMP", "TIFF", "SVG", "ZIP", "RAR", "7Z", "TAR", "GZ", "MDB", "ACCDB", "SQL", "DBF"]
)

# Campo para ingresar el tamaño del archivo (en MB con validación)
size_input = st.text_input(
    "Tamaño del archivo (MB)",
    value="10",
    max_chars=5,
    help="El tamaño máximo permitido es de 1 GB (1024 MB)."
)

# Validación del tamaño y generación de archivo
if st.button("Generar Archivo"):
    try:
        size_mb = int(size_input)

        if size_mb == 0:
            st.error("El tamaño debe ser mayor que 0 MB.")
        elif size_mb > MAX_SIZE_MB:
            st.error("El tamaño máximo permitido es de 1 GB (1024 MB).")
        else:
            file_content = generate_dummy_file(size_mb, file_format)
            filename = f"archivo_dummy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_format.lower()}"
            
            # Descargar el archivo directamente desde Streamlit
            st.download_button(
                label="Descargar archivo",
                data=file_content,
                file_name=filename,
                mime="application/octet-stream"
            )
            st.success(f"{filename} generado exitosamente.")
    except ValueError:
        st.error("Por favor, ingrese un tamaño válido en números enteros.")

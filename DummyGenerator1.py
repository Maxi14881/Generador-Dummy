import os
import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st
from datetime import datetime

# Configuración del tema (opcional)
st.set_page_config(
    page_title="Generador de Archivos",
    page_icon="📄",
)

# Título y logotipo
st.image("Screenshot_46.jpg", width=705)


# Aquí continúa tu lógica de generación de archivos...


# Tamaño máximo permitido en KB (10 GB)
MAX_SIZE_KB = 10240000  # 10,240,000 KB

# Función para generar un archivo PDF
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Generado por Maxi Matrero, https://www.youtube.com/@QAtotheSoftware")
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Función para generar diferentes tipos de archivos
def generate_file(size_kb, file_format):
    block_size = min(10 * 1024 * 1024, size_kb * 1024)  # Bloques de hasta 10 MB
    header_map = {
        "PDF": b"",  # Se generará aparte si es PDF
        "TXT": b"",
        "DOCX": b"",
        "RTF": b"",
        "ODT": b"",
        "XLSX": b"\x09\x08\x10\x00",
        "CSV": b"\x09\x08\x10\x00",
        "MP3": b"\x49\x44\x33",
        "WAV": b"\x49\x44\x33",
        "AAC": b"\x49\x44\x33",
        "FLAC": b"\x49\x44\x33",
        "OGG": b"\x49\x44\x33",
        "WMA": b"\x49\x44\x33",
        "MP4": b"\x00\x00\x00\x18ftypmp42",
        "AVI": b"\x00\x00\x00\x18ftypmp42",
        "MKV": b"\x00\x00\x00\x18ftypmp42",
        "MOV": b"\x00\x00\x00\x18ftypmp42",
        "WMV": b"\x00\x00\x00\x18ftypmp42",
        "FLV": b"\x00\x00\x00\x18ftypmp42",
        "JPEG": b"\x89PNG\r\n\x1a\n",
        "PNG": b"\x89PNG\r\n\x1a\n",
        "GIF": b"\x89PNG\r\n\x1a\n",
        "BMP": b"\x89PNG\r\n\x1a\n",
        "TIFF": b"\x89PNG\r\n\x1a\n",
        "SVG": b"\x89PNG\r\n\x1a\n",
        "ZIP": b"PK\x03\x04",
        "RAR": b"PK\x03\x04",
        "7Z": b"PK\x03\x04",
        "TAR": b"PK\x03\x04",
        "GZ": b"PK\x03\x04",
        "MDB": b"SQLite format 3\x00",
        "ACCDB": b"SQLite format 3\x00",
        "SQL": b"SQLite format 3\x00",
        "DBF": b"SQLite format 3\x00"
    }

    if file_format == "PDF":
        return generate_pdf()  # Genera el PDF usando ReportLab
    else:
        header = header_map.get(file_format, b"")
        file_content = header + bytearray((size_kb * 1024) - len(header))
        return file_content

# Interfaz de Streamlit
st.title("Generador de Archivos Dummy")
file_format = st.selectbox(
    "Selecciona el tipo de archivo",
    ["PDF", "TXT", "DOCX", "RTF", "ODT", "XLSX", "CSV", "MP3", "WAV", "AAC", "FLAC", "OGG", "WMA",
     "MP4", "AVI", "MKV", "MOV", "WMV", "FLV", "JPEG", "PNG", "GIF", "BMP", "TIFF", "SVG", "ZIP", "RAR", "7Z", "TAR", "GZ", "MDB", "ACCDB", "SQL", "DBF"]
)

# Campo para ingresar el tamaño del archivo (texto con validación)
size_input = st.text_input(
    "Tamaño del archivo (KB)",
    value="1000",
    max_chars=8,
    help="El tamaño máximo permitido es de 10 GB (10,240,000 KB)."
)

# Validación del tamaño y generación de archivo
if st.button("Generar Archivo"):
    try:
        size_kb = int(size_input)

       
        print(size_kb,size_input,MAX_SIZE_KB)
        if size_kb > MAX_SIZE_KB:
            st.error("El tamaño máximo permitido es de 10 GB (10,240,000 KB).")
        else:
            file_content = generate_file(size_kb, file_format)
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

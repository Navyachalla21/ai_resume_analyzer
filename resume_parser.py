import pypdf
import docx

def extract_text_from_pdf(file_path_or_buffer) -> str:
    """Extracts all text from a PDF resume, page by page."""
    reader = pypdf.PdfReader(file_path_or_buffer)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_path_or_buffer) -> str:
    """Extracts all text from a DOCX resume, paragraph by paragraph."""
    document = docx.Document(file_path_or_buffer)
    text = ""
    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_resume_text(uploaded_file) -> str:
    """
    Detects file type (PDF or DOCX) from the filename and extracts text accordingly.
    'uploaded_file' is a Streamlit UploadedFile object.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
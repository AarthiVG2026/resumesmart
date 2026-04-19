"""
Robust PDF parser with multiple fallback strategies.
Tries PyPDF2 → pdfplumber → pdfminer → basic extraction.
"""
import re
from io import BytesIO


def extract_text_from_pdf(file):
    """
    Extracts text from an uploaded PDF file.
    Uses multiple libraries as fallbacks to maximize compatibility.
    """
    if hasattr(file, 'seek'):
        file.seek(0)
    file_content = file.read()

    if not file_content:
        raise Exception("The file appears to be empty. Please upload a valid PDF.")

    text = ""

    # --- Strategy 1: pdfplumber (best for complex layouts) ---
    try:
        import pdfplumber
        with pdfplumber.open(BytesIO(file_content)) as pdf:
            pages_text = []
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    pages_text.append(t)
            text = "\n".join(pages_text).strip()
        if len(text) > 30:
            return text
    except Exception:
        pass

    # --- Strategy 2: PyPDF2 ---
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(BytesIO(file_content))
        parts = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                parts.append(t)
        text = "\n".join(parts).strip()
        if len(text) > 30:
            return text
    except Exception:
        pass

    # --- Strategy 3: pdfminer ---
    try:
        from pdfminer.high_level import extract_text as pdfminer_extract
        text = pdfminer_extract(BytesIO(file_content)).strip()
        if len(text) > 30:
            return text
    except Exception:
        pass

    # --- All strategies exhausted ---
    if len(text) > 10:
        # Return whatever we managed to get
        return text

    raise Exception(
        "Could not extract text from this PDF. Your file may be a scanned image. "
        "Please save your resume as a text-based PDF (not a scanned image/photo) and try again. "
        "Tip: In Word or Google Docs, use 'Save/Export as PDF' to create a text-based PDF."
    )


def split_into_sections(text):
    """
    Splits resume text into sections based on common header keywords.
    """
    SECTION_HEADERS = {
        'education':      ['education', 'academic', 'qualification', 'degree', 'schooling'],
        'experience':     ['experience', 'employment', 'work history', 'professional experience', 'career', 'internship'],
        'projects':       ['projects', 'portfolio', 'personal projects', 'key projects'],
        'skills':         ['skills', 'technical skills', 'competencies', 'expertise', 'technologies', 'tools'],
        'certifications': ['certifications', 'certificates', 'licenses', 'accreditation', 'courses'],
        'summary':        ['summary', 'profile', 'objective', 'about me', 'introduction', 'overview'],
        'achievements':   ['achievements', 'accomplishments', 'awards', 'honors', 'recognition'],
        'contact':        ['contact', 'personal information', 'personal details'],
    }

    lines = text.split('\n')
    sections = {}
    current_section = 'other'
    current_content = []

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Only treat short lines as potential headers (headers are rarely > 50 chars)
        matched_section = None
        if len(line_stripped) < 60:
            for section_name, keywords in SECTION_HEADERS.items():
                for keyword in keywords:
                    if keyword in line_lower:
                        matched_section = section_name
                        break
                if matched_section:
                    break

        if matched_section:
            if current_content:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append('\n'.join(current_content))
            current_section = matched_section
            current_content = []
        else:
            if line_stripped:
                current_content.append(line_stripped)

    if current_content:
        if current_section not in sections:
            sections[current_section] = []
        sections[current_section].append('\n'.join(current_content))

    return sections

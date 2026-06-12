# tests/test_file_validation.py

from app import allowed_file

def test_pdf_allowed():
    assert allowed_file(
        "resume.pdf"
    )

def test_docx_allowed():
    assert allowed_file(
        "resume.docx"
    )

def test_txt_not_allowed():
    assert not allowed_file(
        "resume.txt"
    )

def test_png_not_allowed():
    assert not allowed_file(
        "image.png"
    )
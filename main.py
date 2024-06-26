from typing import Optional
from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
import base64

app = FastAPI()

def split_pdf_into_10_pages(pdf_file):
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    chunks = []

    for start_page in range(0, total_pages, 10):
        writer = PdfWriter()
        end_page = min(start_page + 10, total_pages)

        for page in range(start_page, end_page):
            writer.add_page(reader.pages[page])

        buffer = BytesIO()
        writer.write(buffer)
        chunk_bytes = buffer.getvalue()
        chunk_base64 = base64.b64encode(chunk_bytes).decode('utf-8')
        chunks.append(chunk_base64)

    return chunks

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/split_pdf",
          summary="Split PDF into 50-page chunks",
          description="Upload a PDF file to split it into 50-page chunks",
          response_description="Base64-encoded byte arrays of the PDF chunks")
async def split_pdf(pdf_file: UploadFile = File(...)):
    pdf_chunks = split_pdf_into_10_pages(pdf_file.file)
    return {"chunks": pdf_chunks}
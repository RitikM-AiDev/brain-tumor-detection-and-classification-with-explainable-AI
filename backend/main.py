from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import markdown2
import pdfkit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect_tumor(image_bytes):
    tumor_detected = True

    return tumor_detected


def get_ai_report(tumor_detected):
    if tumor_detected == True:

        report = "YES"

    else:

        report = "NO"


    return report

def generate_pdf(ai_text):

    html = markdown2.markdown(ai_text)

    pdf_file = "brain_tumor_report.pdf"

    pdfkit.from_string(html, pdf_file)

    return pdf_file


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    tumor_detected = detect_tumor(contents)
    ai_report = get_ai_report(tumor_detected)
    pdf_file = generate_pdf(ai_report)

    return FileResponse(
        pdf_file,
        media_type="application/pdf",
        filename="brain_tumor_report.pdf"
    )
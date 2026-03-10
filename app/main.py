from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
import shutil
from fastapi.staticfiles import StaticFiles

from app.resume_parser import parse_resume
from app.jd_parser import extract_keywords
from app.similarity import calculate_similarity


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()

@app.post("/analyze")
async def analyze(resume: UploadFile, job_description: str = Form(...)):

    path = f"temp_{resume.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    resume_text = parse_resume(path)

    keywords = extract_keywords(job_description)

    similarity = calculate_similarity(resume_text, job_description)

    ats_score = round(float(similarity) * 100, 2)

    missing_keywords = [
        k for k in keywords if k not in resume_text.lower()
    ]

    return {
        "ATS Score": ats_score,
        "Missing Keywords": missing_keywords[:10]
    }
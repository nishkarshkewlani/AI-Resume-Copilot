# AI Resume Copilot

An NLP-powered web application that compares a resume with a job description and highlights potential areas for improvement. It combines semantic similarity with basic keyword matching to help students review how closely their resume reflects a target role.

> **Important:** The displayed “ATS match score” is a similarity-based estimate produced by this project. It is not an actual score from an applicant tracking system, a hiring decision, or a probability of being shortlisted.

## Features

- Upload a resume in **PDF** or **DOCX** format.
- Extract readable text from the uploaded document.
- Extract noun and proper-noun terms from the job description using spaCy.
- Compare resume and job-description text using sentence embeddings.
- Return a similarity-based match score and up to 10 potentially missing terms.
- Use a simple web interface built with HTML and CSS.

## How it works

1. **Resume upload:** The user uploads a PDF or DOCX and pastes a job description.
2. **Text extraction:** `pdfplumber` extracts text from PDFs; `python-docx` reads paragraph text from DOCX files.
3. **Keyword extraction:** spaCy's `en_core_web_sm` model selects noun and proper-noun tokens from the job description.
4. **Semantic comparison:** `sentence-transformers/all-MiniLM-L6-v2` creates embeddings for the resume and job description. Scikit-learn computes cosine similarity.
5. **Results:** The API returns the similarity score multiplied by 100 and up to 10 terms not found as substrings in the extracted resume text.

## Tech stack

- **Backend:** Python, FastAPI, Uvicorn
- **NLP:** spaCy, Sentence Transformers
- **Similarity:** scikit-learn cosine similarity
- **Document parsing:** pdfplumber, python-docx
- **Frontend:** HTML, CSS
- **Deployment configuration:** Render (`render.yaml`), Procfile

## Project structure

```text
AI-Resume-Copilot-main/
├── app/
│   ├── main.py           # FastAPI routes: / and /analyze
│   ├── resume_parser.py  # PDF/DOCX text extraction
│   ├── jd_parser.py      # spaCy keyword/term extraction
│   └── similarity.py     # Sentence Transformer + cosine similarity
├── static/css/style.css  # Styles
├── templates/index.html  # Web interface
├── requirements.txt
├── render.yaml
└── Procfile
```

## Setup and run locally

Use Python 3.10 or 3.11 if you encounter compatibility issues with ML dependencies.

```bash
# 1. Clone the repository and enter its directory
git clone <YOUR_REPOSITORY_URL>
cd AI-Resume-Copilot-main

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux (run this instead of the Windows command)
source .venv/bin/activate

# 3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Download the spaCy English model
python -m spacy download en_core_web_sm

# 5. Start the development server
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser. FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## API

### `GET /`

Serves the web interface.

### `POST /analyze`

Accepts multipart form data containing:
- `resume`: PDF or DOCX file
- `job_description`: job-description text

Example response:

```json
{
  "ATS Score": 68.42,
  "Missing Keywords": ["python", "database", "testing"]
}
```

The numbers and terms above are illustrative only; results depend on the input documents.

## How to interpret the score

The score is cosine similarity between two sentence embeddings, scaled to a 0–100 display. It measures semantic closeness in the model's embedding space. It is **not** a validated ATS score. It can also be affected by document length, wording, and extraction quality.

The missing-term list uses basic substring matching. It may miss synonyms and multiword skills, and it can flag terms that are present in a different form.

## Current limitations

- Scanned/image-only PDFs are not OCR-processed, so they may produce little or no extracted text.
- DOCX parsing currently reads paragraph text and may omit content in tables, headers, footers, or embedded objects.
- Keyword extraction is a simple POS-based approach, not a curated skills taxonomy.
- Missing-term matching does not understand synonyms, context, or word boundaries.
- The uploaded file is saved using a filename-derived temporary path; production use should validate file types and names, enforce size limits, use safe unique temporary files, and delete them after processing.
- The current implementation does not provide a validated hiring prediction or guarantee that a resume will pass an employer's screening system.

## Potential improvements

- Add safer upload validation, unique temporary files, and cleanup.
- Add OCR for scanned resumes and improve table/header extraction.
- Normalize skills and multiword phrases; support synonyms and exact token matching.
- Show matched and missing skills with explanations instead of a single score alone.
- Add automated tests, file-size limits, error handling, and evaluation on a documented benchmark.
- Evaluate ranking quality against human-labelled resume/job-description pairs before making performance claims.

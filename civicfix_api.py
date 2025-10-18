"""
CivicFix API Backend - Connects AI model to frontend
Run with: uvicorn civicfix_api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO
import base64
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(title="CivicFix AI API", version="1.0")

# Enable CORS (allows frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model once at startup
print("🚀 Loading AI model...")
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
print("✅ Model loaded successfully!")


def _load_image_from_source(image_source: str) -> Image.Image:
    """Support data URLs (base64), http(s) URLs, and local file paths."""
    try:
        if not image_source:
            raise ValueError("Empty image source")

        if image_source.startswith("data:"):
            # data:[<mediatype>][;base64],<data>
            header, b64data = image_source.split(",", 1)
            if ";base64" in header:
                raw = base64.b64decode(b64data)
                return Image.open(BytesIO(raw)).convert("RGB")
            else:
                return Image.open(BytesIO(b64data.encode())).convert("RGB")

        if image_source.startswith("http://") or image_source.startswith("https://"):
            response = requests.get(image_source, timeout=10)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGB")

        # Otherwise assume it's a local file path
        if os.path.exists(image_source):
            return Image.open(image_source).convert("RGB")

        raise ValueError("Unsupported image source or file not found")
    except Exception:
        raise


def _analyze_image_obj(img: Image.Image, image_url: Optional[str] = None):
    """Run classifier and construct standardized response payload."""
    predictions = classifier(img, top_k=6)

    detected_issue = "general civic issue"
    confidence = 0.0
    assigned_dept = "General Administration"
    priority = "Medium"

    for pred in predictions:
        label = pred['label'].lower()
        score = pred['score']

        for keyword, mapping in ISSUE_MAPPING.items():
            if keyword in label:
                detected_issue = label
                confidence = score
                assigned_dept = mapping['department']
                priority = mapping['priority']
                break

        if confidence > 0:
            break

    if confidence == 0 and predictions:
        detected_issue = predictions[0]['label']
        confidence = predictions[0]['score']

    import time
    ticket_id = f"TKT-{int(time.time()) % 1000000}"

    result = {
        "status": "success",
        "image_url": image_url,
        "ai_analysis": {
            "detected_issue": detected_issue,
            "confidence": f"{confidence:.2f}",
            "all_scores": [
                {"label": pred['label'], "score": f"{pred['score']:.2f}"}
                for pred in predictions
            ]
        },
        "assigned_ticket": {
            "ticket_id": ticket_id,
            "priority": priority,
            "department": assigned_dept,
            "status": "Pending Assignment",
            "estimated_resolution": "48-72 hours"
        }
    }
    return result

# Civic issue mapping
ISSUE_MAPPING = {
    "pothole": {
        "category": "Roads > Pothole",
        "department": "Roads & Transport Department",
        "priority": "High"
    },
    "road": {
        "category": "Roads > Damage",
        "department": "Roads & Transport Department",
        "priority": "High"
    },
    "garbage": {
        "category": "Waste > Overflowing Bin",
        "department": "Sanitation Department",
        "priority": "Medium"
    },
    "trash": {
        "category": "Waste > Illegal Dumping",
        "department": "Sanitation Department",
        "priority": "High"
    },
}

# Request model
class AnalyzeRequest(BaseModel):
    image_url: str

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "CivicFix AI API is running"
    }

@app.post("/analyze")
async def analyze_image(request: AnalyzeRequest):
    try:
        image_url = request.image_url
        print(f"📥 Loading image from source: {image_url}")
        img = _load_image_from_source(image_url)

        print("🧠 Running AI classification...")
        result = _analyze_image_obj(img, image_url)
        print(f"✅ Analysis complete: {result['ai_analysis']['detected_issue']}")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/upload")
async def analyze_upload(file: UploadFile = File(...)):
    """Accept multipart file uploads and analyze the image."""
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents)).convert("RGB")
        result = _analyze_image_obj(img, image_url=None)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
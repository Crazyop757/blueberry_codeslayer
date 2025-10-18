"""
CivicFix API Backend - Connects AI model to frontend
Run with: uvicorn civicfix_api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import requests
from io import BytesIO

# Initialize FastAPI app
app = FastAPI(title="CivicFix AI API", version="1.0")

# Enable CORS (allows frontend to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model once at startup
print("🚀 Loading AI model...")
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
print("✅ Model loaded successfully!")

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
        
        # Download image
        print(f"📥 Downloading image: {image_url}")
        response = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(response.content))
        
        # Run AI classification
        print("🧠 Running AI classification...")
        predictions = classifier(img, top_k=6)
        
        # Smart mapping
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
        
        if confidence == 0:
            detected_issue = predictions[0]['label']
            confidence = predictions[0]['score']
        
        # Generate ticket ID
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
        
        print(f"✅ Analysis complete: {detected_issue}")
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
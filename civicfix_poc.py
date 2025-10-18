"""
CivicFix API Backend - Connects AI model to frontend
Run with: uvicorn civicfix_api:app --reload --host 0.0.0.0 --port 8000
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
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI model once at startup (not on every request)
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
    "water": {
        "category": "Water > Flooding",
        "department": "Water & Sewage Department",
        "priority": "Critical"
    },
    "flood": {
        "category": "Water > Flooding",
        "department": "Water & Sewage Department",
        "priority": "Critical"
    },
    "tree": {
        "category": "Parks > Fallen Tree",
        "department": "Parks & Recreation Department",
        "priority": "Medium"
    },
    "light": {
        "category": "Infrastructure > Street Light",
        "department": "Electrical Department",
        "priority": "Low"
    },
    "street": {
        "category": "Roads > General Issue",
        "department": "Roads & Transport Department",
        "priority": "Medium"
    }
}

# Request model
class AnalyzeRequest(BaseModel):
    image_url: str

# Response model
class AnalyzeResponse(BaseModel):
    status: str
    image_url: str
    ai_analysis: dict
    assigned_ticket: dict

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "CivicFix AI API is running",
        "endpoints": {
            "analyze": "/analyze (POST)",
            "health": "/ (GET)"
        }
    }

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_image(request: AnalyzeRequest):
    """
    Main AI endpoint: Analyzes civic issue from image URL
    """
    try:
        image_url = request.image_url
        
        # Download and process image
        print(f"📥 Downloading image: {image_url}")
        response = requests.get(image_url, timeout=10)
        img = Image.open(BytesIO(response.content))
        
        # Run AI classification
        print("🧠 Running AI classification...")
        predictions = classifier(img, top_k=6)
        
        # Smart mapping to civic issues
        detected_issue = "general civic issue"
        confidence = 0.0
        assigned_dept = "General Administration"
        priority = "Medium"
        
        # Match predictions to civic issue categories
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
        
        # If no match, use top prediction
        if confidence == 0:
            detected_issue = predictions[0]['label']
            confidence = predictions[0]['score']
        
        # Generate ticket ID
        import time
        ticket_id = f"TKT-{int(time.time()) % 1000000}"
        
        # Build response
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
        
        print(f"✅ Analysis complete: {detected_issue} ({confidence:.2%})")
        return result
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to download image: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Run with: uvicorn civicfix_api:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🏙️  Starting CivicFix API Server")
    print("="*60)
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Docs available at: http://localhost:8000/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
# CivicFix - AI-Powered Urban Issue Management 🏙️🤖

Transform civic issues into action with AI-powered classification and automated routing.

## 🚀 Features

- **AI Image Classification**: Automatically identifies civic issues from images
- **Smart Routing**: Assigns issues to appropriate departments
- **Priority Management**: Intelligent priority assignment based on issue type
- **Real-time Analysis**: Fast processing using Vision Transformer models

## 📋 Tech Stack

**Backend:**
- FastAPI (Python)
- Transformers (Hugging Face)
- Vision Transformer (ViT) Model
- PyTorch

**Frontend:**
- React.js
- Tailwind CSS
- Lucide React Icons

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the API server
uvicorn civicfix_api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd civicfix-frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🌐 Deployment on Render

### Step 1: Prepare Your Repository

1. Push all code to GitHub:
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Deploy Backend (FastAPI)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `civicfix-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn civicfix_api:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Choose Free or paid plan
5. Click **"Create Web Service"**
6. Wait for deployment (5-10 minutes for first deploy due to model download)
7. **Copy the API URL** (e.g., `https://civicfix-api.onrender.com`)

### Step 3: Deploy Frontend (React)

1. In Render Dashboard, click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure the static site:
   - **Name**: `civicfix-frontend`
   - **Build Command**: `cd civicfix-frontend && npm install && npm run build`
   - **Publish Directory**: `civicfix-frontend/build`
4. Add Environment Variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL from Step 2 (e.g., `https://civicfix-api.onrender.com`)
5. Click **"Create Static Site"**
6. Wait for deployment (3-5 minutes)

### Step 4: Update CORS Settings

After deployment, update the backend CORS settings in `civicfix_api.py` to include your frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend-url.onrender.com",
        "http://localhost:3000"  # For local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then commit and push:
```bash
git add civicfix_api.py
git commit -m "Update CORS settings for production"
git push origin main
```

Render will automatically redeploy your backend.

## 📝 Important Notes

### First Deployment Time
- **Backend**: Takes 5-10 minutes on first deploy (downloads AI model)
- **Frontend**: Takes 3-5 minutes
- **Free Tier**: Services sleep after 15 minutes of inactivity (takes ~30s to wake up)

### Free Tier Limitations
- Services sleep after inactivity
- 750 hours/month of usage
- Model loads on each wake-up (~30s delay)

### Performance Tips
- Use paid Render plans to prevent sleeping
- Consider caching the AI model
- Optimize image sizes before upload

## 🔧 Environment Variables

### Backend (.env)
```env
PORT=8000
```

### Frontend (.env)
```env
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

## 🧪 Testing

Test your deployed API:
```bash
curl https://your-api-url.onrender.com/
```

Expected response:
```json
{
  "status": "online",
  "message": "CivicFix AI API is running"
}
```

## 📖 API Documentation

Once deployed, visit:
- API Docs: `https://your-api-url.onrender.com/docs`
- ReDoc: `https://your-api-url.onrender.com/redoc`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify all dependencies in `requirements.txt`
- Ensure Python version matches `runtime.txt`

### Frontend can't connect to backend
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS settings in backend
- Ensure backend service is running

### Model loading issues
- First load takes time (downloading model)
- Check Render logs for progress
- Verify sufficient memory allocation

## 📧 Support

For issues or questions, please open a GitHub issue.
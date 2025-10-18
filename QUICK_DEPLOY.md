# 🎯 Quick Start: Deploy CivicFix to Render

## ⚡ Quick Overview
Deploy in **3 simple steps**:
1. Deploy Backend (Python API)
2. Deploy Frontend (React App)
3. Connect them together

---

## 📦 Step 1: Deploy Backend API (5-10 minutes)

### Go to Render
1. Visit: https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select: `blueberry_codeslayer`

### Configure Service
```
Name:           civicfix-api
Runtime:        Python 3
Build Command:  pip install -r requirements.txt
Start Command:  uvicorn civicfix_api:app --host 0.0.0.0 --port $PORT
Plan:           Free (or Starter $7/mo for no sleeping)
```

### Deploy & Save URL
- Click **"Create Web Service"**
- Wait for "✅ Model loaded successfully!" in logs
- **📋 COPY YOUR API URL**: `https://civicfix-api-xxxx.onrender.com`

---

## 🎨 Step 2: Deploy Frontend (3-5 minutes)

### Go to Render
1. Click **"New +"** → **"Static Site"**
2. Select same repository: `blueberry_codeslayer`

### Configure Site
```
Name:             civicfix-frontend
Build Command:    cd civicfix-frontend && npm install && npm run build
Publish Directory: civicfix-frontend/build
```

### Add Environment Variable
```
Key:   REACT_APP_API_URL
Value: https://civicfix-api-xxxx.onrender.com  ← Your backend URL from Step 1
```

### Deploy & Save URL
- Click **"Create Static Site"**
- **📋 COPY YOUR FRONTEND URL**: `https://civicfix-frontend-xxxx.onrender.com`

---

## 🔗 Step 3: Connect Frontend & Backend (2 minutes)

### Update CORS Settings
Open `civicfix_api.py` and update line 18-19:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://civicfix-frontend-xxxx.onrender.com",  # ← Add your frontend URL
        "http://localhost:3000"
    ],
```

### Push Changes
```bash
git add civicfix_api.py
git commit -m "Update CORS for production"
git push origin main
```

Wait 2-3 minutes for Render to auto-deploy.

---

## ✅ Test Your Deployment

1. Visit your frontend URL: `https://civicfix-frontend-xxxx.onrender.com`
2. Click a test image or upload one
3. Click "Analyze with AI"
4. See real-time AI results! 🎉

---

## 🆘 Common Issues

### "Failed to analyze image"
- Check backend is running (visit backend URL directly)
- Verify `REACT_APP_API_URL` is set correctly in frontend settings
- Check browser console (F12) for CORS errors

### "Service Unavailable" 
- Free tier sleeps after 15 min → Wait 30s for wake up
- First request after sleep takes longer (model loading)

### CORS Errors
- Update `allow_origins` in `civicfix_api.py`
- Must match exact frontend URL (with https://)
- Commit and push changes

---

## 💰 Cost Breakdown

### Free Tier (Great for demos)
- ✅ 750 hours/month
- ⚠️ Services sleep after 15 min
- ⚠️ 30s cold start time
- **Cost: $0/month**

### Starter Tier (Production ready)
- ✅ No sleeping
- ✅ Instant responses
- ✅ Better performance
- **Cost: $7/month per service = $14/month total**

---

## 📚 Full Documentation

For detailed steps, see: `DEPLOYMENT_CHECKLIST.md`

---

## 🎊 You're Done!

Your AI-powered civic management platform is now live!

**Share your app:**
- Frontend: `https://your-frontend-url.onrender.com`
- API Docs: `https://your-backend-url.onrender.com/docs`

**Next steps:**
- Add custom domain
- Set up monitoring
- Share with users!

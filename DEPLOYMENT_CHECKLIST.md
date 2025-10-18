# 🚀 Render Deployment Checklist

## Prerequisites
- [ ] GitHub account created
- [ ] Render account created (sign up at https://render.com)
- [ ] Code pushed to GitHub repository

## Backend Deployment (FastAPI API)

### 1. Create Web Service on Render
- [ ] Log in to Render Dashboard (https://dashboard.render.com)
- [ ] Click **"New +"** button → Select **"Web Service"**
- [ ] Connect your GitHub repository
- [ ] Select the `blueberry_codeslayer` repository

### 2. Configure Backend Service
Fill in the following settings:

- **Name**: `civicfix-api` (or your preferred name)
- **Region**: Choose closest to your users (e.g., Oregon USA, Frankfurt EU)
- **Branch**: `main`
- **Root Directory**: Leave empty (root of repository)
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  uvicorn civicfix_api:app --host 0.0.0.0 --port $PORT
  ```
- **Plan**: 
  - [ ] Free (good for testing, sleeps after 15 min inactivity)
  - [ ] Starter ($7/month, no sleeping)

### 3. Advanced Settings (Optional)
- **Health Check Path**: `/` (checks if API is online)
- **Auto-Deploy**: Yes (recommended - auto deploys on git push)

### 4. Deploy Backend
- [ ] Click **"Create Web Service"**
- [ ] Wait 5-10 minutes (first deploy downloads AI model ~2GB)
- [ ] Check logs for "✅ Model loaded successfully!"
- [ ] **IMPORTANT**: Copy your backend URL (e.g., `https://civicfix-api.onrender.com`)

### 5. Test Backend
- [ ] Visit: `https://your-api-url.onrender.com/`
- [ ] Should see: `{"status":"online","message":"CivicFix AI API is running"}`
- [ ] Visit: `https://your-api-url.onrender.com/docs` (FastAPI docs)

---

## Frontend Deployment (React Static Site)

### 1. Create Static Site on Render
- [ ] In Render Dashboard, click **"New +"** → Select **"Static Site"**
- [ ] Connect the same GitHub repository
- [ ] Select the `blueberry_codeslayer` repository

### 2. Configure Frontend Service
Fill in the following settings:

- **Name**: `civicfix-frontend` (or your preferred name)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Build Command**: 
  ```
  cd civicfix-frontend && npm install && npm run build
  ```
- **Publish Directory**: 
  ```
  civicfix-frontend/build
  ```

### 3. Add Environment Variables
- [ ] Click **"Advanced"** or **"Environment"** section
- [ ] Add variable:
  - **Key**: `REACT_APP_API_URL`
  - **Value**: `https://your-backend-url.onrender.com` (from backend step 4)

### 4. Deploy Frontend
- [ ] Click **"Create Static Site"**
- [ ] Wait 3-5 minutes for deployment
- [ ] Copy your frontend URL (e.g., `https://civicfix-frontend.onrender.com`)

### 5. Test Frontend
- [ ] Visit your frontend URL
- [ ] Try uploading an image or using a test image
- [ ] Verify AI analysis works

---

## Post-Deployment Configuration

### Update CORS Settings
- [ ] Open `civicfix_api.py` in your code editor
- [ ] Find the CORS middleware section (around line 18)
- [ ] Update `allow_origins` to include your frontend URL:
  ```python
  allow_origins=[
      "https://your-frontend-url.onrender.com",
      "http://localhost:3000"
  ],
  ```
- [ ] Save, commit, and push:
  ```bash
  git add civicfix_api.py
  git commit -m "Update CORS for production"
  git push origin main
  ```
- [ ] Render will auto-deploy (wait 2-3 minutes)

---

## Verification

### Backend Checks
- [ ] Backend URL is accessible
- [ ] `/` endpoint returns status
- [ ] `/docs` shows API documentation
- [ ] Logs show model loaded successfully

### Frontend Checks
- [ ] Frontend URL loads the app
- [ ] Can see the upload interface
- [ ] Test images are clickable
- [ ] Image analysis works end-to-end

### Integration Checks
- [ ] Frontend successfully calls backend
- [ ] No CORS errors in browser console (F12)
- [ ] AI analysis returns results
- [ ] Results display correctly on frontend

---

## Troubleshooting

### Backend Issues

**Service won't start:**
- Check Render logs for Python errors
- Verify `requirements.txt` has all dependencies
- Ensure start command is correct

**Model loading fails:**
- Free tier may have memory limits
- Consider upgrading to Starter plan ($7/month)
- Check logs for specific error messages

**Slow first response:**
- Normal on free tier (service sleeps after 15 min)
- Service takes ~30s to wake up and load model
- Upgrade to paid plan to prevent sleeping

### Frontend Issues

**Build fails:**
- Check Node version compatibility
- Verify `package.json` is correct
- Check Render build logs for npm errors

**Can't connect to backend:**
- Verify `REACT_APP_API_URL` is set correctly
- Check backend CORS settings
- Open browser console (F12) for error messages

**Environment variable not working:**
- Rebuild the static site after adding env vars
- Env vars must start with `REACT_APP_`
- Clear browser cache

### CORS Errors

If you see CORS errors in browser console:
1. Update `allow_origins` in `civicfix_api.py`
2. Include your exact frontend URL
3. Commit and push changes
4. Wait for backend to redeploy

---

## Monitoring & Maintenance

### Monitor Your Services
- [ ] Set up email notifications in Render settings
- [ ] Check logs regularly for errors
- [ ] Monitor response times

### Free Tier Limitations
- Services sleep after 15 min inactivity
- 750 hours/month total across all services
- Slower cold starts (~30s)
- 512MB RAM for web services

### Optimization Tips
- Upgrade to paid plan to prevent sleeping
- Use image optimization on frontend
- Consider caching strategies
- Monitor and optimize model loading time

---

## Next Steps

- [ ] Add custom domain (optional)
- [ ] Set up monitoring/analytics
- [ ] Add authentication if needed
- [ ] Implement rate limiting
- [ ] Add error tracking (e.g., Sentry)
- [ ] Create staging environment

---

## URLs to Save

**Backend API**: `https://__________________.onrender.com`
**Frontend**: `https://__________________.onrender.com`
**GitHub Repo**: `https://github.com/Crazyop757/blueberry_codeslayer`

---

## Support Resources

- Render Documentation: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- React Build Guide: https://create-react-app.dev/docs/deployment/

---

✅ **Deployment Complete!** Your CivicFix app is now live!

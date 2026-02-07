# 🌐 Deployment Guide

Complete guide for deploying your AI Spam Detection application to production.

## 🎯 Deployment Architecture

```
┌─────────────────┐
│   Frontend      │
│   (Vercel)      │──┐
└─────────────────┘  │
                     │
┌─────────────────┐  │
│   Backend API   │  │
│   (Railway)     │◄─┘
└─────────────────┘  │
         │           │
         │           │
         ▼           ▼
┌─────────────────┐ ┌──────────────┐
│   ML Service    │ │   MongoDB    │
│   (Railway)     │ │   (Atlas)    │
└─────────────────┘ └──────────────┘
```

---

## 📦 Pre-Deployment Checklist

- [ ] Test all features locally
- [ ] Train ML model with production data
- [ ] Set strong JWT secret
- [ ] Configure MongoDB Atlas
- [ ] Update CORS origins
- [ ] Enable environment variables
- [ ] Test API endpoints
- [ ] Build frontend for production
- [ ] Configure error logging
- [ ] Set up monitoring

---

## 🗄️ Step 1: Deploy MongoDB (Atlas)

### 1.1 Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a new cluster (M0 Free tier)
4. Wait for cluster creation (~5 minutes)

### 1.2 Configure Database

1. **Create Database User:**
   - Security → Database Access
   - Add New Database User
   - Username: `spamdetection`
   - Password: Generate secure password
   - Role: Read and write to any database

2. **Configure Network Access:**
   - Security → Network Access
   - Add IP Address
   - Allow Access from Anywhere: `0.0.0.0/0` (for development)
   - For production: Add specific IPs

3. **Get Connection String:**
   - Click "Connect"
   - Choose "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

```
mongodb+srv://spamdetection:<password>@cluster0.xxxxx.mongodb.net/spam-detection?retryWrites=true&w=majority
```

---

## 🐍 Step 2: Deploy ML Service (Railway)

### 2.1 Prepare ML Service

Add `Procfile` to `ml-service/`:
```
web: python src/app.py
```

Add `runtime.txt` to `ml-service/`:
```
python-3.11.0
```

Update `src/app.py` to use PORT from environment:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 2.2 Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Create New Project
4. Deploy from GitHub repo
5. Select `ml-service` folder
6. Add Environment Variables:
   - `PORT`: 5000
   - `PYTHON_VERSION`: 3.11.0

7. Wait for deployment
8. Copy your ML service URL: `https://your-ml-service.railway.app`

### 2.3 Upload Trained Model

**Option A:** Include in Git (if < 100MB)
- Add models to git
- Push to GitHub

**Option B:** Upload to cloud storage
- Use AWS S3 or Google Cloud Storage
- Download during deployment

---

## 🔧 Step 3: Deploy Backend (Railway)

### 3.1 Prepare Backend

Add to `backend/package.json`:
```json
{
  "engines": {
    "node": "18.x"
  },
  "scripts": {
    "start": "node src/server.js"
  }
}
```

### 3.2 Deploy to Railway

1. Railway Dashboard → New Project
2. Deploy from GitHub repo
3. Select `backend` folder
4. Add Environment Variables:
   ```
   NODE_ENV=production
   PORT=3001
   MONGODB_URI=<your-atlas-connection-string>
   JWT_SECRET=<generate-strong-secret>
   ML_SERVICE_URL=<your-ml-service-url>
   ```

5. Deploy
6. Copy your backend URL: `https://your-backend.railway.app`

### 3.3 Generate Strong JWT Secret

```bash
# Node.js
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"

# Or use online generator:
# https://randomkeygen.com/
```

---

## ⚛️ Step 4: Deploy Frontend (Vercel)

### 4.1 Prepare Frontend

Create `vercel.json` in `frontend/`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

Update `package.json`:
```json
{
  "scripts": {
    "build": "react-scripts build"
  }
}
```

### 4.2 Deploy to Vercel

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import Project
4. Select your GitHub repo
5. Set Root Directory: `frontend`
6. Add Environment Variable:
   ```
   REACT_APP_API_URL=<your-backend-url>
   ```

7. Deploy
8. Your app is live! 🎉

---

## 🔐 Step 5: Security Hardening

### 5.1 Update Backend CORS

In `backend/src/server.js`:
```javascript
const cors = require('cors');

app.use(cors({
  origin: ['https://your-frontend.vercel.app'],
  credentials: true
}));
```

### 5.2 Add Rate Limiting

```bash
npm install express-rate-limit
```

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

### 5.3 Environment Security

- ✅ Never commit `.env` files
- ✅ Use strong passwords
- ✅ Rotate secrets regularly
- ✅ Enable 2FA on all accounts
- ✅ Use HTTPS everywhere

---

## 📊 Step 6: Monitoring & Logging

### 6.1 Error Tracking (Sentry)

```bash
npm install @sentry/node
```

```javascript
const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: process.env.NODE_ENV
});
```

### 6.2 Logging (Winston)

```bash
npm install winston
```

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

---

## 🧪 Step 7: Testing Production

### Test Checklist

1. **Frontend:**
   - [ ] Landing page loads
   - [ ] Sign up works
   - [ ] Login works
   - [ ] Protected routes work
   - [ ] Dashboard loads
   - [ ] Prediction works
   - [ ] History displays

2. **Backend:**
   - [ ] Health check responds
   - [ ] Auth endpoints work
   - [ ] Protected endpoints require token
   - [ ] Predictions save to database

3. **ML Service:**
   - [ ] Health check responds
   - [ ] Predictions are accurate
   - [ ] Response time < 1s

---

## 📱 Step 8: Custom Domain (Optional)

### Frontend (Vercel)

1. Go to Vercel Dashboard
2. Select your project
3. Settings → Domains
4. Add your domain
5. Update DNS records

### Backend (Railway)

1. Railway Dashboard
2. Your project → Settings
3. Add custom domain
4. Update DNS records

---

## 🔄 Step 9: CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy Frontend
      run: vercel --prod
      env:
        VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
    
    - name: Deploy Backend
      run: railway up
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 💰 Cost Estimation

### Free Tier (Development)

- **MongoDB Atlas:** Free (M0 tier - 512MB)
- **Railway:** $5/month credit (ML + Backend)
- **Vercel:** Free (Frontend)

**Total: ~$0-5/month**

### Production (1000 users/day)

- **MongoDB Atlas:** $25/month (M10 tier)
- **Railway:** $20/month (both services)
- **Vercel:** Free (unless high traffic)

**Total: ~$45/month**

---

## 🚨 Troubleshooting

### Frontend can't connect to backend

- Check CORS configuration
- Verify environment variables
- Ensure HTTPS on both

### ML predictions fail

- Verify ML service is running
- Check model files uploaded
- Review ML service logs

### Database connection errors

- Check MongoDB Atlas whitelist
- Verify connection string
- Check network access settings

---

## 📈 Performance Optimization

1. **Frontend:**
   - Enable code splitting
   - Optimize images
   - Use CDN for assets
   - Enable caching

2. **Backend:**
   - Add Redis caching
   - Optimize database queries
   - Use connection pooling
   - Enable compression

3. **ML Service:**
   - Batch predictions
   - Model optimization
   - Caching frequent queries
   - Use GPU if available

---

## 🎉 Success!

Your application is now deployed and accessible to the world! 🌍

**Next Steps:**
- Monitor performance
- Collect user feedback
- Iterate on features
- Scale as needed

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)

---

Need help? Open an issue or reach out! 🆘

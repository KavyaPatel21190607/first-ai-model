# 🚀 Complete Setup Guide - AI Spam Detection Application

This guide will walk you through setting up the entire application stack from scratch.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (3.8 or higher) - [Download](https://www.python.org/)
- **MongoDB** (local or Atlas account) - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/)

## 📁 Project Structure

```
Basic-2-ML/
├── ml-service/          # Python ML Service
├── backend/             # Node.js API
├── frontend/            # React Application
└── README.md
```

## 🎯 Step-by-Step Setup

### Step 1: Download Dataset

1. Go to Kaggle: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
2. Download the `spam.csv` file
3. Place it in: `ml-service/data/spam.csv`

### Step 2: Setup ML Service (Python)

```bash
# Navigate to ml-service
cd ml-service

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model
python src/train.py

# Start ML service (keep this running)
python src/app.py
```

The ML service will run on: **http://localhost:5000**

✅ You should see: "ML Spam Detection Service running"

### Step 3: Setup Backend (Node.js)

Open a **new terminal** window:

```bash
# Navigate to backend
cd backend

# Install dependencies
npm install

# Create .env file
copy .env.example .env    # Windows
cp .env.example .env      # macOS/Linux

# Edit .env file with your settings:
# - Set MONGODB_URI (see MongoDB setup below)
# - Set JWT_SECRET (any random string)
# - ML_SERVICE_URL should be http://localhost:5000

# Start backend server (keep this running)
npm run dev
```

The backend will run on: **http://localhost:3001**

✅ You should see: "Backend API Server Running"

#### MongoDB Setup Options:

**Option A: Local MongoDB**
```
MONGODB_URI=mongodb://localhost:27017/spam-detection
```

**Option B: MongoDB Atlas (Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create cluster
4. Get connection string
5. Replace `<password>` with your password
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/spam-detection
```

### Step 4: Setup Frontend (React)

Open a **new terminal** window:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file (already exists, verify it)
# Should contain:
# REACT_APP_API_URL=http://localhost:3001

# Start frontend (keep this running)
npm start
```

The frontend will open automatically at: **http://localhost:3000**

✅ You should see the landing page!

## ✅ Verification Checklist

Make sure all three services are running:

1. ✅ **ML Service** - http://localhost:5000
   - Test: Visit http://localhost:5000/health
   - Should return: `{"status": "healthy"}`

2. ✅ **Backend API** - http://localhost:3001
   - Test: Visit http://localhost:3001/api/health
   - Should return JSON with status

3. ✅ **Frontend** - http://localhost:3000
   - Should display the landing page

## 🎮 Using the Application

### First Time User Flow:

1. **Open** http://localhost:3000
2. **Click** "Get Started Free" or "Sign Up"
3. **Create account** with:
   - Name: Your name
   - Email: your@email.com
   - Password: (min 6 characters)
4. **Login** automatically redirects to Dashboard
5. **Enter a message** to test spam detection
6. **View results** with confidence scores
7. **Check history** to see all predictions

### Example Messages to Test:

**Spam Examples:**
```
Congratulations! You've won a $1000 gift card. Click here to claim now!
```
```
URGENT: Your account has been compromised. Verify your identity immediately.
```
```
FREE entry to WIN £1000 cash prize! Text WIN to 12345
```

**Legitimate Examples:**
```
Hey, are we still meeting for lunch tomorrow?
```
```
Can you pick up milk on your way home?
```
```
Thanks for your help yesterday, really appreciate it!
```

## 🔧 Troubleshooting

### ML Service Issues

**Problem:** Model not found error
```bash
# Solution: Retrain the model
cd ml-service
python src/train.py
```

**Problem:** NLTK data not found
```python
# Solution: Download NLTK data (automatic on first run)
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### Backend Issues

**Problem:** MongoDB connection error
```bash
# Solution 1: Check if MongoDB is running (local)
# Windows: Check Services
# macOS: brew services list

# Solution 2: Verify connection string in .env
# Make sure MONGODB_URI is correct
```

**Problem:** Port 3001 already in use
```bash
# Solution: Change port in backend/.env
PORT=3002
```

### Frontend Issues

**Problem:** API connection refused
```bash
# Solution: Verify backend is running on port 3001
# Check REACT_APP_API_URL in frontend/.env
```

**Problem:** npm install fails
```bash
# Solution: Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

## 🚢 Running in Production

### Build Frontend
```bash
cd frontend
npm run build
```

### Environment Variables for Production
```bash
# Backend .env
NODE_ENV=production
MONGODB_URI=<production-mongodb-uri>
JWT_SECRET=<strong-random-secret>
ML_SERVICE_URL=<production-ml-service-url>

# Frontend .env.production
REACT_APP_API_URL=<production-backend-url>
```

## 🧪 Testing the Complete Flow

1. **Start all services** (ML, Backend, Frontend)
2. **Open** http://localhost:3000
3. **Sign up** with test account
4. **Login** and verify redirect to dashboard
5. **Test prediction** with sample message
6. **Verify** result appears with confidence score
7. **Check history** page for saved prediction
8. **Logout** and verify redirect

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [Express.js Documentation](https://expressjs.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Scikit-learn Documentation](https://scikit-learn.org/)

## 🆘 Getting Help

If you encounter issues:

1. Check error messages in terminal
2. Verify all services are running
3. Check browser console for frontend errors
4. Review MongoDB connection
5. Ensure dataset is in correct location

## 🎉 Success!

If you can:
- ✅ Sign up and login
- ✅ Predict spam detection
- ✅ View results with confidence
- ✅ See prediction history

**Congratulations! Your application is fully functional!** 🚀

---

## 🔄 Development Workflow

For daily development:

```bash
# Terminal 1: ML Service
cd ml-service
venv\Scripts\activate
python src/app.py

# Terminal 2: Backend
cd backend
npm run dev

# Terminal 3: Frontend
cd frontend
npm start
```

## 🌟 Next Steps

- Deploy to cloud (Heroku, Vercel, AWS)
- Add more features (analytics, charts)
- Implement model retraining
- Add email integration
- Create admin dashboard
- Set up CI/CD pipeline

Happy coding! 💻✨

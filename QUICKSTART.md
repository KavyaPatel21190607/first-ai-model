# 🚀 Quick Start Guide

Get your AI Spam Detection application running in 5 minutes!

## ⚡ Super Quick Setup

### 1. Download Dataset (2 minutes)

1. Visit: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
2. Download `spam.csv`
3. Place in: `ml-service/data/spam.csv`

### 2. Terminal 1 - ML Service

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/train.py
python src/app.py
```

✅ Running on http://localhost:5000

### 3. Terminal 2 - Backend

```bash
cd backend
npm install
copy .env.example .env
# Edit .env: Add MongoDB URI and JWT secret
npm run dev
```

✅ Running on http://localhost:3001

### 4. Terminal 3 - Frontend

```bash
cd frontend
npm install
npm start
```

✅ Opens at http://localhost:3000

## 🎯 Test It!

1. Go to http://localhost:3000
2. Click "Get Started Free"
3. Create account
4. Enter: "CONGRATULATIONS! You won $1000!"
5. See the magic ✨

## 🔥 Pro Tips

- Keep all 3 terminals running
- Use MongoDB Atlas for quick cloud database
- Test with example messages in dashboard

## 📝 Environment Variables

**backend/.env:**
```env
MONGODB_URI=mongodb://localhost:27017/spam-detection
JWT_SECRET=your-secret-key-here
ML_SERVICE_URL=http://localhost:5000
PORT=3001
```

**frontend/.env:**
```env
REACT_APP_API_URL=http://localhost:3001
```

## ❓ Issues?

- **Model not found?** → Run `python src/train.py`
- **Port in use?** → Change port in .env files
- **MongoDB error?** → Use MongoDB Atlas (cloud)

Need detailed help? See [SETUP_GUIDE.md](SETUP_GUIDE.md)

🎉 **You're ready to detect spam!**

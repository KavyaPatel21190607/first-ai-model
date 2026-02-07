# 🚀 AI Spam Detection - Full Stack ML Application

A production-grade, full-stack AI/ML web application that intelligently detects spam messages using machine learning. Built with modern architecture and exceptional UX.

![Tech Stack](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

## ✨ Features

- 🧠 **AI-Powered Spam Detection** - Trained from scratch using Naive Bayes
- 🔐 **Secure Authentication** - JWT-based user authentication
- 📊 **Confidence Scoring** - Get prediction confidence levels
- 📜 **History Tracking** - View all your past predictions
- 🎨 **Modern UI/UX** - Smooth animations and micro-interactions
- 📱 **Fully Responsive** - Works seamlessly on all devices

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────┐
│   React     │────▶│  Node.js +   │────▶│   Python    │────▶│  ML      │
│  Frontend   │     │   Express    │     │  ML Service │     │  Model   │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   MongoDB    │
                    └──────────────┘
```

## 📁 Project Structure

```
spam-detection/
├── frontend/              # React application
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API communication
│   │   ├── utils/        # Helper functions
│   │   └── App.jsx       # Main app component
│   └── package.json
│
├── backend/              # Node.js + Express API
│   ├── src/
│   │   ├── controllers/  # Request handlers
│   │   ├── middleware/   # Auth & validation
│   │   ├── models/       # MongoDB schemas
│   │   ├── routes/       # API routes
│   │   └── server.js     # Entry point
│   └── package.json
│
├── ml-service/           # Python ML service
│   ├── data/            # Dataset storage
│   ├── models/          # Trained models
│   ├── src/
│   │   ├── train.py     # Model training
│   │   ├── predict.py   # Prediction logic
│   │   └── app.py       # Flask API
│   └── requirements.txt
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v16+)
- Python (3.8+)
- MongoDB (local or Atlas)
- Git

### 1. Clone the Repository

```bash
cd "c:\Users\Patel Kavya\Desktop\Basic-2-ML"
```

### 2. Setup ML Service

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Download dataset and train model
python src/train.py

# Start ML service
python src/app.py
# Runs on http://localhost:5000
```

### 3. Setup Backend

```bash
cd backend
npm install

# Create .env file with:
# MONGODB_URI=your_mongodb_connection_string
# JWT_SECRET=your_secret_key
# ML_SERVICE_URL=http://localhost:5000

npm run dev
# Runs on http://localhost:3001
```

### 4. Setup Frontend

```bash
cd frontend
npm install

# Create .env file with:
# REACT_APP_API_URL=http://localhost:3001

npm start
# Runs on http://localhost:3000
```

## 🎯 ML Model Details

- **Algorithm**: Naive Bayes (MultinomialNB)
- **Dataset**: Kaggle SMS Spam Collection
- **Features**: TF-IDF Vectorization
- **Preprocessing**: Lowercasing, punctuation removal, stopwords, tokenization
- **Performance**: ~97% accuracy on test set

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user

### Predictions
- `POST /api/predict` - Analyze message (protected)
- `GET /api/predictions/history` - Get user history (protected)

### Health
- `GET /api/health` - Service health check

## 🎨 Tech Stack

**Frontend:**
- React.js
- Axios
- React Router
- Framer Motion (animations)
- CSS3 with modern animations

**Backend:**
- Node.js
- Express.js
- MongoDB with Mongoose
- JWT for authentication
- Bcrypt for password hashing

**ML Service:**
- Python 3.8+
- Scikit-learn
- NLTK
- Flask
- Pandas, NumPy

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
npm test

# ML service tests
cd ml-service
pytest
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build

# Backend & ML Service ready as-is
```

## 🚢 Deployment

The application is designed to be deployed on:
- **Frontend**: Vercel, Netlify, or AWS S3
- **Backend**: Heroku, Railway, or AWS EC2
- **ML Service**: Docker container on AWS, GCP, or Azure
- **Database**: MongoDB Atlas

## 📚 Learning Outcomes

This project demonstrates:
- ✅ End-to-end ML system design
- ✅ Full-stack development skills
- ✅ Clean architecture principles
- ✅ Modern UX design patterns
- ✅ Real-world ML deployment
- ✅ Secure authentication implementation

## 🎓 Future Enhancements

- [ ] Admin dashboard for model management
- [ ] Real-time model retraining
- [ ] Multi-language support
- [ ] Email header analysis
- [ ] Analytics and charts
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 📄 License

MIT License - feel free to use this project for learning!

## 👨‍💻 Author

Built with ❤️ to demonstrate production-level AI/ML engineering
-Kavya Patel

---

⭐ Star this repo if you find it helpful!

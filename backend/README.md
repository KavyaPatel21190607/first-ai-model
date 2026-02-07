# Backend API - Spam Detection

Node.js + Express backend API with MongoDB for user authentication and prediction management.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Configure environment variables in `.env`:
- Set MongoDB connection string
- Set JWT secret
- Set ML service URL

4. Start server:
```bash
# Development
npm run dev

# Production
npm start
```

## API Documentation

### Authentication

#### Signup
```
POST /api/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}
```

### Predictions (Protected Routes)

All prediction endpoints require authentication header:
```
Authorization: Bearer <your-jwt-token>
```

#### Make Prediction
```
POST /api/predictions/predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "Congratulations! You won $1000!"
}
```

#### Get History
```
GET /api/predictions/history?page=1&limit=20
Authorization: Bearer <token>
```

#### Get Statistics
```
GET /api/predictions/stats
Authorization: Bearer <token>
```

#### Delete Prediction
```
DELETE /api/predictions/:id
Authorization: Bearer <token>
```

### Health Check
```
GET /api/health
```

## Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── User.js           # User schema
│   │   └── Prediction.js     # Prediction schema
│   ├── routes/
│   │   ├── auth.js           # Authentication routes
│   │   └── predictions.js    # Prediction routes
│   ├── middleware/
│   │   ├── auth.js           # JWT authentication
│   │   └── validation.js     # Input validation
│   └── server.js             # Express server
├── .env.example
├── package.json
└── README.md
```

## Technologies

- **Express.js** - Web framework
- **MongoDB + Mongoose** - Database
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Express Validator** - Input validation
- **Helmet** - Security headers
- **CORS** - Cross-origin requests

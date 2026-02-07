# API Documentation

Complete API reference for the Spam Detection Backend.

## Base URL

```
http://localhost:3001/api
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

---

## Authentication Endpoints

### Sign Up

Create a new user account.

**Endpoint:** `POST /auth/signup`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User created successfully",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Error Responses:**
- `400` - Email already registered
- `400` - Validation errors

---

### Login

Authenticate and receive JWT token.

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

**Error Responses:**
- `401` - Invalid email or password
- `400` - Validation errors

---

## Prediction Endpoints (Protected)

### Make Prediction

Analyze a message for spam detection.

**Endpoint:** `POST /predictions/predict`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "message": "Congratulations! You've won a $1000 gift card!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "prediction": "spam",
    "confidence": 0.9876,
    "isSpam": true,
    "spamProbability": 0.9876,
    "hamProbability": 0.0124,
    "timestamp": "2026-02-07T10:30:00.000Z"
  }
}
```

**Error Responses:**
- `401` - Unauthorized (no token or invalid token)
- `400` - Message is empty or too long
- `503` - ML service unavailable

---

### Get Prediction History

Retrieve user's prediction history with pagination.

**Endpoint:** `GET /predictions/history`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (optional) - Page number (default: 1)
- `limit` (optional) - Items per page (default: 20, max: 100)

**Example:**
```
GET /predictions/history?page=1&limit=10
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "predictions": [
      {
        "_id": "507f1f77bcf86cd799439011",
        "message": "Win $1000 now!",
        "prediction": "spam",
        "confidence": 0.9876,
        "spamProbability": 0.9876,
        "hamProbability": 0.0124,
        "createdAt": "2026-02-07T10:30:00.000Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 150,
      "pages": 8
    }
  }
}
```

**Error Responses:**
- `401` - Unauthorized

---

### Get Statistics

Get user's prediction statistics.

**Endpoint:** `GET /predictions/stats`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "total": 150,
    "spam": 45,
    "ham": 105,
    "spamPercentage": "30.00",
    "averageConfidence": "0.9234",
    "recentActivity": 23
  }
}
```

**Error Responses:**
- `401` - Unauthorized

---

### Delete Prediction

Delete a specific prediction from history.

**Endpoint:** `DELETE /predictions/:id`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Prediction deleted successfully"
}
```

**Error Responses:**
- `401` - Unauthorized
- `404` - Prediction not found

---

## Health Check

### API Health

Check if the API is running.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "Spam Detection Backend API",
  "timestamp": "2026-02-07T10:30:00.000Z",
  "mongodb": "connected"
}
```

---

## Error Response Format

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

### Validation Errors

For validation errors (e.g., signup/login):

```json
{
  "success": false,
  "errors": [
    {
      "field": "email",
      "message": "Please provide a valid email"
    },
    {
      "field": "password",
      "message": "Password must be at least 6 characters"
    }
  ]
}
```

---

## Status Codes

- `200` - Success
- `201` - Created (signup)
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (auth required)
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (ML service down)

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider adding:

- Per-user rate limits
- IP-based rate limits
- Token bucket algorithm

---

## Examples

### cURL Examples

**Signup:**
```bash
curl -X POST http://localhost:3001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Predict (with token):**
```bash
curl -X POST http://localhost:3001/api/predictions/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "message": "Win $1000 now!"
  }'
```

### JavaScript (Axios) Examples

**Signup:**
```javascript
const response = await axios.post('http://localhost:3001/api/auth/signup', {
  name: 'John Doe',
  email: 'john@example.com',
  password: 'password123'
});

const token = response.data.token;
localStorage.setItem('token', token);
```

**Predict:**
```javascript
const token = localStorage.getItem('token');

const response = await axios.post(
  'http://localhost:3001/api/predictions/predict',
  { message: 'Win $1000 now!' },
  {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  }
);

console.log(response.data);
```

---

## Postman Collection

Import this collection into Postman:

1. Create new collection: "Spam Detection API"
2. Add base URL variable: `{{base_url}}` = `http://localhost:3001/api`
3. Add token variable: `{{token}}` (set after login)
4. Add all endpoints from this documentation

---

## Security Considerations

1. **Always use HTTPS in production**
2. **Store JWT secret securely**
3. **Implement rate limiting**
4. **Add request validation**
5. **Sanitize user inputs**
6. **Use environment variables**
7. **Enable CORS properly**
8. **Implement refresh tokens**
9. **Add request logging**
10. **Monitor for suspicious activity**

---

For more details, see the [main README](README.md) or [setup guide](SETUP_GUIDE.md).

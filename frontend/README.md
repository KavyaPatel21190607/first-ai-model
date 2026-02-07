# Frontend - React Application

Modern, responsive React frontend for the AI Spam Detection application.

## Features

- 🎨 Modern UI with animations (Framer Motion)
- 🔐 JWT authentication
- 📱 Fully responsive design
- 🎯 Real-time spam detection
- 📊 User dashboard & history
- 🌈 Beautiful gradients and micro-interactions
- 🔔 Toast notifications

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
Create `.env` file:
```
REACT_APP_API_URL=http://localhost:3001
```

3. Start development server:
```bash
npm start
```

The app will open at http://localhost:3000

## Build for Production

```bash
npm run build
```

The optimized build will be in the `build/` folder.

## Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── manifest.json
├── src/
│   ├── components/
│   │   ├── Navbar.jsx        # Navigation bar
│   │   └── ProtectedRoute.jsx # Route protection
│   ├── context/
│   │   └── AuthContext.js     # Auth state management
│   ├── pages/
│   │   ├── Landing.jsx        # Landing page
│   │   ├── Login.jsx          # Login page
│   │   ├── Signup.jsx         # Signup page
│   │   ├── Dashboard.jsx      # Main dashboard
│   │   └── History.jsx        # Prediction history
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.jsx                # Main app component
│   ├── index.js               # Entry point
│   └── index.css              # Global styles
├── package.json
└── README.md
```

## Key Dependencies

- **React** - UI library
- **React Router** - Routing
- **Axios** - HTTP client
- **Framer Motion** - Animations
- **React Toastify** - Notifications

## Available Routes

- `/` - Landing page
- `/login` - Login page
- `/signup` - Signup page
- `/dashboard` - Main dashboard (protected)
- `/history` - Prediction history (protected)

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:3001)

## Development Tips

- Hot reload is enabled by default
- Use React DevTools for debugging
- All API calls go through the API service layer
- Protected routes automatically redirect to login

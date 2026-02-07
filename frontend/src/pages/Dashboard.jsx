import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { predictionService } from '../services/api';
import { toast } from 'react-toastify';
import { useAuth } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const [message, setMessage] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!message.trim()) {
      toast.error('Please enter a message');
      return;
    }

    setLoading(true);
    setPrediction(null);

    try {
      const response = await predictionService.predict(message);
      setPrediction(response.data);
      toast.success('Prediction complete! 🎯');
    } catch (error) {
      toast.error(error.response?.data?.error || 'Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessage('');
    setPrediction(null);
  };

  const exampleMessages = [
    "Congratulations! You've won a $1000 gift card. Click here to claim now!",
    "Hey, are we still meeting for lunch tomorrow?",
    "URGENT: Your account has been compromised. Verify immediately!",
    "Can you pick up milk on your way home?"
  ];

  const loadExample = (example) => {
    setMessage(example);
    setPrediction(null);
  };

  return (
    <div className="dashboard-page">
      <div className="container">
        <motion.div 
          className="dashboard-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1>Welcome, {user?.name}! 👋</h1>
          <p>Enter a message below to check if it's spam</p>
        </motion.div>

        <div className="dashboard-grid">
          <motion.div 
            className="prediction-section"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="card prediction-card">
              <h2 className="card-title">
                <span className="title-icon">🔍</span>
                Analyze Message
              </h2>

              <form onSubmit={handleSubmit}>
                <div className="input-group">
                  <label htmlFor="message">Enter Message</label>
                  <textarea
                    id="message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type or paste your message here..."
                    maxLength="5000"
                    disabled={loading}
                  />
                  <div className="char-count">
                    {message.length} / 5000 characters
                  </div>
                </div>

                <div className="button-group">
                  <button 
                    type="submit" 
                    className="btn btn-primary btn-full"
                    disabled={loading || !message.trim()}
                  >
                    {loading ? (
                      <>
                        <div className="spinner" style={{ width: '20px', height: '20px' }}></div>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <span>🧠</span>
                        Detect Spam
                      </>
                    )}
                  </button>
                  
                  {message && !loading && (
                    <button 
                      type="button"
                      onClick={handleClear}
                      className="btn btn-secondary"
                    >
                      Clear
                    </button>
                  )}
                </div>
              </form>

              <div className="examples-section">
                <p className="examples-title">Try these examples:</p>
                <div className="examples-grid">
                  {exampleMessages.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => loadExample(example)}
                      className="example-btn"
                      disabled={loading}
                    >
                      {example.substring(0, 50)}...
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div 
            className="result-section"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3, duration: 0.5 }}
          >
            <AnimatePresence mode="wait">
              {prediction ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.5 }}
                  className={`result-card ${prediction.isSpam ? 'spam' : 'ham'}`}
                >
                  <div className="result-icon">
                    {prediction.isSpam ? '❌' : '✅'}
                  </div>
                  
                  <h2 className="result-title">
                    {prediction.isSpam ? 'SPAM DETECTED' : 'NOT SPAM'}
                  </h2>
                  
                  <p className="result-description">
                    {prediction.isSpam 
                      ? 'This message appears to be spam or malicious.'
                      : 'This message looks legitimate and safe.'}
                  </p>

                  <div className="confidence-section">
                    <div className="confidence-header">
                      <span>Confidence Score</span>
                      <span className="confidence-value">
                        {(prediction.confidence * 100).toFixed(2)}%
                      </span>
                    </div>
                    
                    <div className="confidence-bar">
                      <motion.div 
                        className="confidence-fill"
                        initial={{ width: 0 }}
                        animate={{ width: `${prediction.confidence * 100}%` }}
                        transition={{ duration: 1, ease: "easeOut" }}
                      />
                    </div>
                  </div>

                  <div className="probability-grid">
                    <div className="probability-item">
                      <div className="probability-label">Spam Probability</div>
                      <div className="probability-value spam-color">
                        {(prediction.spamProbability * 100).toFixed(2)}%
                      </div>
                    </div>
                    
                    <div className="probability-item">
                      <div className="probability-label">Ham Probability</div>
                      <div className="probability-value ham-color">
                        {(prediction.hamProbability * 100).toFixed(2)}%
                      </div>
                    </div>
                  </div>

                  <div className="result-timestamp">
                    Analyzed on {new Date(prediction.timestamp).toLocaleString()}
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="result-placeholder"
                >
                  <motion.div 
                    className="placeholder-icon"
                    animate={{ 
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0]
                    }}
                    transition={{ 
                      duration: 3,
                      repeat: Infinity,
                      repeatType: "reverse"
                    }}
                  >
                    🎯
                  </motion.div>
                  
                  <h3>Ready to Detect</h3>
                  <p>Enter a message to see AI-powered spam detection in action</p>
                  
                  <div className="features-list">
                    <div className="feature-item">
                      <span className="feature-icon">⚡</span>
                      <span>Instant Results</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-icon">🎯</span>
                      <span>97% Accuracy</span>
                    </div>
                    <div className="feature-item">
                      <span className="feature-icon">🔒</span>
                      <span>100% Private</span>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

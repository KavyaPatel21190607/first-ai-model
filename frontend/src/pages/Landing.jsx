import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Landing.css';

const Landing = () => {
  return (
    <div className="landing-page">
      <motion.div 
        className="hero-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div className="container">
          <motion.div 
            className="hero-content"
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            <motion.div 
              className="hero-icon"
              animate={{ 
                rotate: [0, 10, -10, 0],
                scale: [1, 1.1, 1]
              }}
              transition={{ 
                duration: 3,
                repeat: Infinity,
                repeatType: "reverse"
              }}
            >
              🛡️
            </motion.div>
            
            <h1 className="hero-title">
              Detect Spam with
              <span className="gradient-text"> AI Power</span>
            </h1>
            
            <p className="hero-subtitle">
              Advanced machine learning technology that protects you from unwanted messages.
              Fast, accurate, and intelligent spam detection at your fingertips.
            </p>
            
            <div className="hero-buttons">
              <Link to="/signup" className="btn btn-primary btn-large">
                Get Started Free
                <span className="btn-arrow">→</span>
              </Link>
              <Link to="/login" className="btn btn-secondary btn-large">
                Sign In
              </Link>
            </div>
            
            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-value">97%</div>
                <div className="stat-label">Accuracy</div>
              </div>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <div className="stat-value">&lt;1s</div>
                <div className="stat-label">Response Time</div>
              </div>
              <div className="stat-divider"></div>
              <div className="stat-item">
                <div className="stat-value">24/7</div>
                <div className="stat-label">Available</div>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Powered by Advanced AI</h2>
          
          <div className="features-grid">
            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">🧠</div>
              <h3>Machine Learning</h3>
              <p>Trained on thousands of real spam messages using Naive Bayes algorithm</p>
            </motion.div>

            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">⚡</div>
              <h3>Lightning Fast</h3>
              <p>Get instant predictions with confidence scores in milliseconds</p>
            </motion.div>

            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">🔒</div>
              <h3>Secure & Private</h3>
              <p>Your data is encrypted and stored securely with industry-standard protection</p>
            </motion.div>

            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">📊</div>
              <h3>Track History</h3>
              <p>View all your predictions and analyze patterns over time</p>
            </motion.div>

            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">🎯</div>
              <h3>High Accuracy</h3>
              <p>Achieve 97%+ accuracy with our sophisticated NLP preprocessing</p>
            </motion.div>

            <motion.div 
              className="feature-card"
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <div className="feature-icon">✨</div>
              <h3>Easy to Use</h3>
              <p>Simple, intuitive interface designed for everyone</p>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <motion.div 
            className="cta-content"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            <h2>Ready to Stop Spam?</h2>
            <p>Join thousands of users protecting themselves from unwanted messages</p>
            <Link to="/signup" className="btn btn-primary btn-large">
              Start Detecting Now
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Landing;

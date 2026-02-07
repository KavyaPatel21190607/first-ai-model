import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { predictionService } from '../services/api';
import { toast } from 'react-toastify';
import './History.css';

const History = () => {
  const [predictions, setPredictions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [pagination, setPagination] = useState(null);

  useEffect(() => {
    loadData();
  }, [page]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [historyRes, statsRes] = await Promise.all([
        predictionService.getHistory(page, 10),
        predictionService.getStats()
      ]);
      
      setPredictions(historyRes.data.predictions);
      setPagination(historyRes.data.pagination);
      setStats(statsRes.data);
    } catch (error) {
      toast.error('Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this prediction?')) {
      return;
    }

    try {
      await predictionService.deletePrediction(id);
      toast.success('Prediction deleted');
      loadData();
    } catch (error) {
      toast.error('Failed to delete prediction');
    }
  };

  if (loading && !predictions.length) {
    return (
      <div className="history-page">
        <div className="container">
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading your history...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="container">
        <motion.div 
          className="history-header"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1>Prediction History 📜</h1>
          <p>View and manage all your spam detection results</p>
        </motion.div>

        {stats && (
          <motion.div 
            className="stats-grid"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <div className="stat-content">
                <div className="stat-value">{stats.total}</div>
                <div className="stat-label">Total Predictions</div>
              </div>
            </div>

            <div className="stat-card spam-stat">
              <div className="stat-icon">❌</div>
              <div className="stat-content">
                <div className="stat-value">{stats.spam}</div>
                <div className="stat-label">Spam Detected</div>
              </div>
            </div>

            <div className="stat-card ham-stat">
              <div className="stat-icon">✅</div>
              <div className="stat-content">
                <div className="stat-value">{stats.ham}</div>
                <div className="stat-label">Legitimate Messages</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🎯</div>
              <div className="stat-content">
                <div className="stat-value">{(stats.averageConfidence * 100).toFixed(1)}%</div>
                <div className="stat-label">Avg Confidence</div>
              </div>
            </div>
          </motion.div>
        )}

        {predictions.length === 0 ? (
          <motion.div 
            className="empty-state"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="empty-icon">📭</div>
            <h3>No predictions yet</h3>
            <p>Start analyzing messages to see your history here</p>
          </motion.div>
        ) : (
          <>
            <motion.div 
              className="history-list"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              {predictions.map((pred, index) => (
                <motion.div
                  key={pred._id}
                  className={`history-item ${pred.prediction}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  whileHover={{ scale: 1.02 }}
                >
                  <div className="history-icon">
                    {pred.prediction === 'spam' ? '❌' : '✅'}
                  </div>
                  
                  <div className="history-content">
                    <div className="history-message">
                      {pred.message.substring(0, 100)}
                      {pred.message.length > 100 && '...'}
                    </div>
                    
                    <div className="history-meta">
                      <span className={`prediction-badge ${pred.prediction}`}>
                        {pred.prediction === 'spam' ? 'SPAM' : 'LEGITIMATE'}
                      </span>
                      
                      <span className="confidence-badge">
                        {(pred.confidence * 100).toFixed(2)}% confidence
                      </span>
                      
                      <span className="timestamp">
                        {new Date(pred.createdAt).toLocaleString()}
                      </span>
                    </div>
                  </div>

                  <button 
                    onClick={() => handleDelete(pred._id)}
                    className="delete-btn"
                    title="Delete"
                  >
                    🗑️
                  </button>
                </motion.div>
              ))}
            </motion.div>

            {pagination && pagination.pages > 1 && (
              <div className="pagination">
                <button 
                  onClick={() => setPage(page - 1)}
                  disabled={page === 1}
                  className="btn btn-secondary"
                >
                  Previous
                </button>
                
                <span className="page-info">
                  Page {page} of {pagination.pages}
                </span>
                
                <button 
                  onClick={() => setPage(page + 1)}
                  disabled={page === pagination.pages}
                  className="btn btn-secondary"
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default History;

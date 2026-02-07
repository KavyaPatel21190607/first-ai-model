const express = require('express');
const axios = require('axios');
const auth = require('../middleware/auth');
const Prediction = require('../models/Prediction');
const { validatePrediction, handleValidationErrors } = require('../middleware/validation');

const router = express.Router();

// ML Service URL
const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000';

// Predict endpoint (protected)
router.post('/predict', auth, validatePrediction, handleValidationErrors, async (req, res) => {
  try {
    const { message } = req.body;
    const userId = req.userId;
    
    // Call ML service
    const mlResponse = await axios.post(`${ML_SERVICE_URL}/predict`, {
      message
    });
    
    if (!mlResponse.data.success) {
      return res.status(500).json({
        success: false,
        error: 'ML service returned an error'
      });
    }
    
    const { prediction, confidence, details } = mlResponse.data;
    
    // Save prediction to database
    const predictionDoc = new Prediction({
      userId,
      message,
      prediction,
      confidence,
      spamProbability: details.spam_probability,
      hamProbability: details.ham_probability
    });
    
    await predictionDoc.save();
    
    // Return result
    res.json({
      success: true,
      data: {
        id: predictionDoc._id,
        prediction,
        confidence,
        isSpam: prediction === 'spam',
        spamProbability: details.spam_probability,
        hamProbability: details.ham_probability,
        timestamp: predictionDoc.createdAt
      }
    });
    
  } catch (error) {
    console.error('Prediction error:', error);
    
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({
        success: false,
        error: 'ML service is not available. Please ensure it is running.'
      });
    }
    
    res.status(500).json({
      success: false,
      error: 'Prediction failed'
    });
  }
});

// Get prediction history (protected)
router.get('/history', auth, async (req, res) => {
  try {
    const userId = req.userId;
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const skip = (page - 1) * limit;
    
    // Get predictions
    const predictions = await Prediction.find({ userId })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-userId');
    
    // Get total count
    const total = await Prediction.countDocuments({ userId });
    
    res.json({
      success: true,
      data: {
        predictions,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }
    });
    
  } catch (error) {
    console.error('History error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch history'
    });
  }
});

// Get user statistics (protected)
router.get('/stats', auth, async (req, res) => {
  try {
    const userId = req.userId;
    
    // Get statistics
    const total = await Prediction.countDocuments({ userId });
    const spamCount = await Prediction.countDocuments({ userId, prediction: 'spam' });
    const hamCount = await Prediction.countDocuments({ userId, prediction: 'ham' });
    
    // Get average confidence
    const avgConfidence = await Prediction.aggregate([
      { $match: { userId } },
      { $group: { _id: null, avgConfidence: { $avg: '$confidence' } } }
    ]);
    
    // Get recent activity (last 7 days)
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    
    const recentCount = await Prediction.countDocuments({
      userId,
      createdAt: { $gte: sevenDaysAgo }
    });
    
    res.json({
      success: true,
      data: {
        total,
        spam: spamCount,
        ham: hamCount,
        spamPercentage: total > 0 ? ((spamCount / total) * 100).toFixed(2) : 0,
        averageConfidence: avgConfidence.length > 0 ? avgConfidence[0].avgConfidence.toFixed(4) : 0,
        recentActivity: recentCount
      }
    });
    
  } catch (error) {
    console.error('Stats error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch statistics'
    });
  }
});

// Delete prediction (protected)
router.delete('/:id', auth, async (req, res) => {
  try {
    const userId = req.userId;
    const predictionId = req.params.id;
    
    const prediction = await Prediction.findOneAndDelete({
      _id: predictionId,
      userId
    });
    
    if (!prediction) {
      return res.status(404).json({
        success: false,
        error: 'Prediction not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Prediction deleted successfully'
    });
    
  } catch (error) {
    console.error('Delete error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to delete prediction'
    });
  }
});

module.exports = router;

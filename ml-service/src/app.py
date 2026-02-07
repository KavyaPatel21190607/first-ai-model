from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
from predict import SpamPredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize predictor
try:
    predictor = SpamPredictor(model_dir='../models')
    print("✅ ML Service initialized successfully!")
except Exception as e:
    print(f"❌ Error initializing predictor: {e}")
    predictor = None

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    if predictor is None:
        return jsonify({
            'status': 'error',
            'message': 'ML model not loaded. Please train the model first.'
        }), 503
    
    return jsonify({
        'status': 'healthy',
        'service': 'ML Spam Detection Service',
        'version': '1.0.0'
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    
    Expected JSON:
    {
        "message": "Your text message here"
    }
    
    Returns:
    {
        "success": true,
        "prediction": "spam" or "ham",
        "confidence": 0.95,
        "details": {
            "spam_probability": 0.95,
            "ham_probability": 0.05
        }
    }
    """
    if predictor is None:
        return jsonify({
            'success': False,
            'error': 'ML model not loaded. Please train the model first.'
        }), 503
    
    try:
        # Get message from request
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "message" field in request body'
            }), 400
        
        message = data['message']
        
        # Validate message
        if not message or not message.strip():
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        if len(message) > 5000:
            return jsonify({
                'success': False,
                'error': 'Message too long (max 5000 characters)'
            }), 400
        
        # Make prediction
        result = predictor.predict(message)
        
        # Format response
        response = {
            'success': True,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'details': {
                'spam_probability': result['spam_probability'],
                'ham_probability': result['ham_probability'],
                'label': result['label']
            },
            'message_preview': message[:100] + '...' if len(message) > 100 else message
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint
    
    Expected JSON:
    {
        "messages": ["message1", "message2", ...]
    }
    """
    if predictor is None:
        return jsonify({
            'success': False,
            'error': 'ML model not loaded'
        }), 503
    
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "messages" field'
            }), 400
        
        messages = data['messages']
        
        if not isinstance(messages, list):
            return jsonify({
                'success': False,
                'error': '"messages" must be an array'
            }), 400
        
        if len(messages) > 100:
            return jsonify({
                'success': False,
                'error': 'Maximum 100 messages per batch'
            }), 400
        
        # Predict
        results = predictor.batch_predict(messages)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """
    Get model performance metrics
    """
    try:
        metrics_path = '../models/metrics.pkl'
        
        if not os.path.exists(metrics_path):
            return jsonify({
                'success': False,
                'error': 'Metrics not available'
            }), 404
        
        with open(metrics_path, 'rb') as f:
            metrics = pickle.load(f)
        
        return jsonify({
            'success': True,
            'metrics': metrics
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting ML Spam Detection Service")
    print("=" * 60)
    print("\n📡 Endpoints available:")
    print("   GET  /health          - Health check")
    print("   POST /predict         - Single prediction")
    print("   POST /batch-predict   - Batch predictions")
    print("   GET  /metrics         - Model metrics")
    print("\n🌐 Service running on http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

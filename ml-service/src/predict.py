import pickle
import os
import re
import nltk
from nltk.corpus import stopwords

class SpamPredictor:
    def __init__(self, model_dir='../models'):
        """
        Load trained model and vectorizer
        """
        # Convert to absolute path based on this file's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isabs(model_dir):
            self.model_dir = os.path.abspath(os.path.join(current_dir, model_dir))
        else:
            self.model_dir = model_dir
            
        # Load stopwords (must match training)
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # Fallback stopwords if NLTK not available
            self.stop_words = {
                'i','me','my','we','our','you','your','he','she','it','they','them',
                'is','are','was','were','be','been','being','have','has','had',
                'do','does','did','a','an','the','and','but','if','or','because',
                'as','until','while','of','at','by','for','with','about','against',
                'between','into','through','during','before','after','to','from'
            }
        
        self.load_model()
    
    def load_model(self):
        """
        Load the trained model and vectorizer
        """
        model_path = os.path.join(self.model_dir, 'spam_classifier.pkl')
        vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Please train the model first using 'python src/train.py'"
            )
        
        if not os.path.exists(vectorizer_path):
            raise FileNotFoundError(
                f"Vectorizer not found at {vectorizer_path}. "
                "Please train the model first using 'python src/train.py'"
            )
        
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        
        print("✅ Model and vectorizer loaded successfully!")
    
    def preprocess_text(self, text):
        """
        Apply the EXACT same preprocessing as training
        """
        # Convert to string and lowercase
        text = str(text).lower()
        
        # KEEP numbers & spam symbols (MUST MATCH TRAINING!)
        text = re.sub(r'[^a-z0-9₹$%!?\s]', ' ', text)
        
        # Simple tokenization (like training)
        tokens = text.split()
        
        # Remove stopwords (NO STEMMING to match training)
        tokens = [w for w in tokens if w not in self.stop_words and len(w) > 2]
        
        return ' '.join(tokens)
    
    def predict(self, message):
        """
        Predict if a message is spam or not
        
        Returns:
            dict: {
                'prediction': 'spam' or 'ham',
                'confidence': float (0-1),
                'label': int (0 or 1)
            }
        """
        # Preprocess
        processed_message = self.preprocess_text(message)
        
        # Vectorize
        message_vec = self.vectorizer.transform([processed_message])
        
        # Predict
        prediction = self.model.predict(message_vec)[0]
        
        # Get probability/confidence
        probabilities = self.model.predict_proba(message_vec)[0]
        confidence = float(max(probabilities))
        
        result = {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'label': int(prediction),
            'confidence': round(confidence, 4),
            'spam_probability': round(float(probabilities[1]), 4),
            'ham_probability': round(float(probabilities[0]), 4)
        }
        
        return result
    
    def batch_predict(self, messages):
        """
        Predict for multiple messages at once
        """
        results = []
        for message in messages:
            results.append(self.predict(message))
        return results

# Test the predictor
if __name__ == '__main__':
    predictor = SpamPredictor()
    
    # Test messages
    test_messages = [
        "Congratulations! You've won a $1000 gift card. Click here to claim now!",
        "Hey, are we still meeting for lunch tomorrow?",
        "URGENT: Your account has been compromised. Verify your identity immediately.",
        "Can you pick up milk on your way home?",
        "FREE entry to WIN £1000 cash prize! Text WIN to 12345"
    ]
    
    print("\n🧪 Testing Spam Predictor:\n")
    print("=" * 70)
    
    for msg in test_messages:
        result = predictor.predict(msg)
        emoji = "❌" if result['prediction'] == 'spam' else "✅"
        
        print(f"\n{emoji} Message: {msg[:60]}...")
        print(f"   Prediction: {result['prediction'].upper()}")
        print(f"   Confidence: {result['confidence']*100:.2f}%")
        print(f"   Spam Probability: {result['spam_probability']*100:.2f}%")
        print("-" * 70)

import os
import pandas as pd
import numpy as np
import pickle
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Try to import NLTK components, but make them optional
try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer
    NLTK_AVAILABLE = True
except:
    NLTK_AVAILABLE = False
    print("⚠️  NLTK data not available, using basic preprocessing")

class SpamDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000)
        self.model = MultinomialNB()
        
        # Try to download and load NLTK data
        self.nltk_available = False
        try:
            # Try to download NLTK data
            try:
                nltk.data.find('corpora/stopwords')
            except:
                try:
                    nltk.download('stopwords', quiet=True)
                except:
                    pass
            
            try:
                nltk.data.find('tokenizers/punkt')
            except:
                try:
                    nltk.download('punkt', quiet=True)
                except:
                    pass
            
            # Try to load NLTK components
            from nltk.corpus import stopwords
            from nltk.stem import PorterStemmer
            from nltk.tokenize import word_tokenize
            
            self.stemmer = PorterStemmer()
            self.stop_words = set(stopwords.words('english'))
            self.nltk_available = True
            print("✅ NLTK components loaded successfully")
        except Exception as e:
            print(f"⚠️  NLTK not fully available, using basic preprocessing: {str(e)[:50]}")
            self.stemmer = None
            # Basic stopwords list as fallback
            self.stop_words = {
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
                'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 
                'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
                'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
                'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 
                'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once'
            }
        
    def preprocess_text(self, text):
        """
        Comprehensive text preprocessing pipeline
        """
        # Lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenization
        if self.nltk_available:
            try:
                from nltk.tokenize import word_tokenize
                tokens = word_tokenize(text)
            except:
                # Fallback to simple split
                tokens = text.split()
        else:
            # Simple tokenization
            tokens = text.split()
        
        # Remove stopwords and stem
        if self.stemmer and self.nltk_available:
            tokens = [
                self.stemmer.stem(word) 
                for word in tokens 
                if word not in self.stop_words and len(word) > 2
            ]
        else:
            # Basic filtering without stemming
            tokens = [
                word 
                for word in tokens 
                if word not in self.stop_words and len(word) > 2
            ]
        
        return ' '.join(tokens)
    
    def load_single_dataset(self, filepath):
        """
        Load a single CSV dataset and normalize it
        """
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except Exception as e:
            print(f"⚠️  Error loading {filepath}: {e}")
            return None
        
        # Handle different column naming conventions
        if 'v1' in df.columns and 'v2' in df.columns:
            # spam.csv format
            df = df[['v1', 'v2']]
            df.columns = ['label', 'message']
        elif 'text' in df.columns and 'spam' in df.columns:
            # emails.csv format
            df = df[['spam', 'text']]
            df.columns = ['label', 'message']
        elif 'label' in df.columns and 'text' in df.columns:
            # spam_ham_dataset.csv format
            df = df[['label', 'text']]
            df.columns = ['label', 'message']
        elif 'label' in df.columns and 'message' in df.columns:
            pass
        elif 'Category' in df.columns and 'Message' in df.columns:
            df.columns = ['label', 'message']
        else:
            print(f"⚠️  Unexpected structure in {filepath}. Columns: {df.columns.tolist()}")
            return None
        
        # Convert labels to binary (handle various formats)
        label_map = {'ham': 0, 'spam': 1, 'Ham': 0, 'Spam': 1, 0: 0, 1: 1, '0': 0, '1': 1}
        df['label'] = df['label'].map(label_map)
        
        # Remove rows with NaN labels or messages
        df = df.dropna(subset=['label', 'message'])
        
        return df
    
    def load_data(self, data_dir='../data'):
        """
        Load and combine all available datasets
        """
        print("📂 Loading all datasets from directory...")
        
        # List of dataset files to load
        dataset_files = ['spam.csv', 'emails.csv', 'spam_ham_dataset.csv']
        
        all_dataframes = []
        
        for filename in dataset_files:
            filepath = os.path.join(data_dir, filename)
            if os.path.exists(filepath):
                print(f"   Loading {filename}...")
                df = self.load_single_dataset(filepath)
                if df is not None:
                    all_dataframes.append(df)
                    print(f"   ✅ {filename}: {len(df)} messages loaded")
            else:
                print(f"   ⚠️  {filename} not found, skipping...")
        
        if not all_dataframes:
            print("❌ No datasets found!")
            return None
        
        # Combine all datasets
        print("\n🔗 Combining all datasets...")
        df = pd.concat(all_dataframes, ignore_index=True)
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['message'])
        duplicates_removed = initial_count - len(df)
        
        print(f"✅ Combined dataset created: {len(df)} messages")
        print(f"   - Duplicates removed: {duplicates_removed}")
        print(f"   - Spam: {(df['label'] == 1).sum()}")
        print(f"   - Ham: {(df['label'] == 0).sum()}")
        
        return df
    
    def train(self, X_train, y_train):
        """
        Train the model
        """
        print("\n🧠 Training Naive Bayes model...")
        self.model.fit(X_train, y_train)
        print("✅ Model trained successfully!")
        
    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance
        """
        print("\n📊 Evaluating model...")
        
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"\n🎯 Model Performance:")
        print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall:    {recall:.4f}")
        print(f"   F1 Score:  {f1:.4f}")
        
        print(f"\n📈 Confusion Matrix:")
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        
        print(f"\n📋 Classification Report:")
        print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': cm.tolist()
        }
    
    def save_model(self, model_dir='../models'):
        """
        Save trained model and vectorizer
        """
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, 'spam_classifier.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        metrics_path = os.path.join(model_dir, 'metrics.pkl')
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        print(f"\n💾 Model saved to: {model_path}")
        print(f"💾 Vectorizer saved to: {vectorizer_path}")

def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("🚀 SPAM DETECTION MODEL TRAINING")
    print("=" * 60)
    
    # Initialize detector
    detector = SpamDetector()
    
    # Load data from all CSV files
    data_dir = '../data'
    
    if not os.path.exists(data_dir):
        print(f"\n❌ Data directory not found: {data_dir}")
        return
    
    df = detector.load_data(data_dir)
    
    if df is None:
        return
    
    # Preprocess messages
    print("\n🔧 Preprocessing messages...")
    df['processed_message'] = df['message'].apply(detector.preprocess_text)
    
    # Split data
    print("✂️  Splitting data (80% train, 20% test)...")
    X = df['processed_message']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Vectorize
    print("🔢 Vectorizing text using TF-IDF...")
    X_train_vec = detector.vectorizer.fit_transform(X_train)
    X_test_vec = detector.vectorizer.transform(X_test)
    
    # Train
    detector.train(X_train_vec, y_train)
    
    # Evaluate
    metrics = detector.evaluate(X_test_vec, y_test)
    
    # Save metrics
    os.makedirs('../models', exist_ok=True)
    with open('../models/metrics.pkl', 'wb') as f:
        pickle.dump(metrics, f)
    
    # Save model
    detector.save_model()
    
    # Optional: Compare with Logistic Regression
    print("\n" + "=" * 60)
    print("🔄 Comparing with Logistic Regression...")
    print("=" * 60)
    
    lr_model = LogisticRegression(max_iter=1000, random_state=42)
    lr_model.fit(X_train_vec, y_train)
    
    y_pred_lr = lr_model.predict(X_test_vec)
    lr_accuracy = accuracy_score(y_test, y_pred_lr)
    
    print(f"\n📊 Logistic Regression Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
    
    if lr_accuracy > metrics['accuracy']:
        print("⚠️  Logistic Regression performed better!")
        print("   Consider using it for production.")
    else:
        print("✅ Naive Bayes is the winner!")
    
    print("\n" + "=" * 60)
    print("✨ Training Complete!")
    print("=" * 60)
    print("\n🎉 Your model is ready to detect spam!")
    print("📍 Next step: Start the ML service with 'python src/app.py'")

if __name__ == '__main__':
    main()

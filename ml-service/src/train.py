import os
import pandas as pd
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

# Optional NLTK
try:
    from nltk.corpus import stopwords
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))
    print("✅ NLTK stopwords loaded")
except:
    STOP_WORDS = {
        'i','me','my','we','our','you','your','he','she','it','they','them',
        'is','are','was','were','be','been','being','have','has','had',
        'do','does','did','a','an','the','and','but','if','or','because',
        'as','until','while','of','at','by','for','with','about','against',
        'between','into','through','during','before','after','to','from'
    }
    print("⚠️ Using fallback stopwords")

class SpamDetector:
    def __init__(self):
        # 🔥 Spam-optimized TF-IDF
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.9,
            sublinear_tf=True,
            max_features=15000
        )

        # 🔥 Tuned Naive Bayes
        self.model = MultinomialNB(alpha=0.3)

    def preprocess_text(self, text):
        """
        Accuracy-focused preprocessing
        """
        text = str(text).lower()

        # KEEP numbers & spam symbols
        text = re.sub(r'[^a-z0-9₹$%!?\s]', ' ', text)

        tokens = text.split()
        tokens = [w for w in tokens if w not in STOP_WORDS and len(w) > 2]

        return " ".join(tokens)

    def load_single_dataset(self, filepath):
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except:
            return None

        if 'v1' in df.columns and 'v2' in df.columns:
            df = df[['v1','v2']]
            df.columns = ['label','message']
        elif 'spam' in df.columns and 'text' in df.columns:
            df = df[['spam','text']]
            df.columns = ['label','message']
        elif 'label' in df.columns and 'text' in df.columns:
            df = df[['label','text']]
            df.columns = ['label','message']
        elif 'Category' in df.columns and 'Message' in df.columns:
            df = df[['Category','Message']]
            df.columns = ['label','message']
        else:
            return None

        label_map = {'ham':0,'spam':1,'Ham':0,'Spam':1,0:0,1:1,'0':0,'1':1}
        df['label'] = df['label'].map(label_map)

        return df.dropna(subset=['label','message'])

    def load_data(self, data_dir='../data'):
        files = ['spam.csv','emails.csv','spam_ham_dataset.csv']
        dfs = []

        for f in files:
            path = os.path.join(data_dir,f)
            if os.path.exists(path):
                df = self.load_single_dataset(path)
                if df is not None:
                    dfs.append(df)
                    print(f"✅ Loaded {f}: {len(df)} rows")

        if not dfs:
            return None

        df = pd.concat(dfs, ignore_index=True)
        df = df.drop_duplicates(subset='message')

        print(f"\n📊 Final Dataset:")
        print(f"   Total: {len(df)}")
        print(f"   Spam : {(df.label==1).sum()}")
        print(f"   Ham  : {(df.label==0).sum()}")

        return df

    def train(self, X, y):
        self.model.fit(X, y)

    def evaluate(self, X, y):
        y_pred = self.model.predict(X)

        acc = accuracy_score(y, y_pred)
        prec = precision_score(y, y_pred)
        rec = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)

        print("\n🎯 Naive Bayes Performance")
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1 Score : {f1:.4f}")

        print("\nConfusion Matrix")
        print(confusion_matrix(y, y_pred))

        print("\nClassification Report")
        print(classification_report(y, y_pred, target_names=['Ham','Spam']))

        return acc

    def save(self, model_dir='../models'):
        os.makedirs(model_dir, exist_ok=True)
        pickle.dump(self.model, open(f"{model_dir}/spam_classifier.pkl","wb"))
        pickle.dump(self.vectorizer, open(f"{model_dir}/vectorizer.pkl","wb"))
        print("\n💾 Model & Vectorizer saved")

def main():
    print("="*60)
    print("🚀 SPAM DETECTION TRAINING (ACCURACY MODE)")
    print("="*60)

    detector = SpamDetector()
    df = detector.load_data('../data')

    if df is None:
        print("❌ No data found")
        return

    print("\n🔧 Preprocessing text...")
    df['clean_text'] = df['message'].apply(detector.preprocess_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df['clean_text'],
        df['label'],
        test_size=0.2,
        stratify=df['label'],
        random_state=42
    )

    print("🔢 Vectorizing...")
    X_train_vec = detector.vectorizer.fit_transform(X_train)
    X_test_vec = detector.vectorizer.transform(X_test)

    print("🧠 Training Naive Bayes...")
    detector.train(X_train_vec, y_train)

    nb_acc = detector.evaluate(X_test_vec, y_test)
    detector.save()

    print("\n" + "="*60)
    print("🔄 Logistic Regression Comparison")
    print("="*60)

    lr = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        C=2.0,
        solver="liblinear"
    )
    lr.fit(X_train_vec, y_train)
    lr_acc = accuracy_score(y_test, lr.predict(X_test_vec))

    print(f"Logistic Regression Accuracy: {lr_acc:.4f}")

    if lr_acc > nb_acc:
        print("⚠️ Logistic Regression is BETTER for accuracy")
    else:
        print("✅ Naive Bayes is BEST")

    print("\n✨ Training Complete")

if __name__ == "__main__":
    main()

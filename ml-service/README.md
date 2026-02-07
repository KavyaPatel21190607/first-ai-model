# ML Service - Spam Detection

Python-based machine learning service for spam detection using Naive Bayes.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download dataset:
- Get the Kaggle SMS Spam Collection dataset
- URL: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
- Place `spam.csv` in the `data/` folder

4. Train model:
```bash
python src/train.py
```

5. Start service:
```bash
python src/app.py
```

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Single message prediction
- `POST /batch-predict` - Multiple message predictions
- `GET /metrics` - Model performance metrics

## Project Structure

```
ml-service/
├── data/
│   └── spam.csv          # Dataset (download from Kaggle)
├── models/
│   ├── spam_classifier.pkl   # Trained model
│   ├── vectorizer.pkl        # TF-IDF vectorizer
│   └── metrics.pkl           # Performance metrics
├── src/
│   ├── train.py          # Model training script
│   ├── predict.py        # Prediction logic
│   └── app.py            # Flask API server
└── requirements.txt
```

## Model Details

- **Algorithm**: Naive Bayes (MultinomialNB)
- **Features**: TF-IDF (3000 features)
- **Preprocessing**: Lowercase, remove punctuation, stopwords, stemming
- **Expected Accuracy**: ~97%

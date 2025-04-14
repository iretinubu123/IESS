from transformers import pipeline

# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]  # Example output: {'label': 'POSITIVE', 'score': 0.98}

# backend/model.py
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import numpy as np

# Load emotion classification model
emotion_model_name = "j-hartmann/emotion-english-distilroberta-base"
emotion_classifier = pipeline("text-classification", 
                             model=emotion_model_name, 
                             return_all_scores=True)

# Optional: Load additional sentiment model
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# Dictionary mapping emotions to musical qualities
EMOTION_TO_MUSICAL_QUALITIES = {
    "joy": ["happy", "upbeat", "energetic"],
    "sadness": ["sad", "melancholic", "slow"],
    "anger": ["intense", "heavy", "powerful"],
    "fear": ["tense", "dark", "atmospheric"],
    "surprise": ["dynamic", "unexpected", "dramatic"],
    "disgust": ["dissonant", "provocative"],
    "neutral": ["balanced", "moderate"]
}

# Dictionary mapping sentiments to musical genres
SENTIMENT_TO_GENRES = {
    "positive": ["pop", "dance", "happy"],
    "neutral": ["indie", "alternative", "ambient"],
    "negative": ["blues", "sad", "emotional"]
}

def analyze_text(text):
    """
    Analyze input text to extract emotions and generate music-related keywords
    
    Args:
        text (str): User input text
        
    Returns:
        dict: Analysis results including emotions, keywords for music search
    """
    # Get emotion scores
    emotion_results = emotion_classifier(text)[0]
    emotions = {item['label']: item['score'] for item in emotion_results}
    
    # Get top emotions (those with scores above average)
    avg_score = sum(emotions.values()) / len(emotions)
    top_emotions = {e: s for e, s in emotions.items() if s > avg_score}
    
    # Get sentiment
    sentiment_result = sentiment_classifier(text)[0]
    sentiment = sentiment_result['label'].lower()
    
    # Generate search keywords based on emotions and sentiment
    search_keywords = []
    
    # Add keywords from top emotions
    for emotion, score in top_emotions.items():
        if emotion in EMOTION_TO_MUSICAL_QUALITIES:
            # Pick keywords proportionally to emotion strength
            num_keywords = min(int(score * 3) + 1, len(EMOTION_TO_MUSICAL_QUALITIES[emotion]))
            search_keywords.extend(EMOTION_TO_MUSICAL_QUALITIES[emotion][:num_keywords])
    
    # Add genre keywords based on sentiment
    if sentiment in SENTIMENT_TO_GENRES:
        search_keywords.extend(SENTIMENT_TO_GENRES[sentiment])
    
    # Process any explicit musical references in the text
    # (For simplicity, we're just checking for some common genres)
    common_genres = ["rock", "pop", "jazz", "hip hop", "rap", "classical", "electronic", "metal", "country", "blues"]
    for genre in common_genres:
        if genre in text.lower():
            search_keywords.append(genre)
    
    return {
        "emotions": emotions,
        "top_emotions": list(top_emotions.keys()),
        "sentiment": sentiment,
        "search_keywords": search_keywords
    }
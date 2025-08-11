# Simplified version using basic NLP
import re
from collections import Counter

def analyze_text(text):
    """Simple text analysis without heavy ML dependencies"""
    
    # Basic emotion keywords
    emotion_keywords = {
        'happy': ['happy', 'joy', 'excited', 'cheerful', 'upbeat', 'positive'],
        'sad': ['sad', 'depressed', 'down', 'melancholy', 'blue', 'lonely'],
        'angry': ['angry', 'mad', 'furious', 'rage', 'annoyed'],
        'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'serene'],
        'energetic': ['energetic', 'pumped', 'hyped', 'active', 'dynamic']
    }
    
    text_lower = text.lower()
    detected_emotions = []
    
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_emotions.append(emotion)
    
    # Default emotions if none detected
    if not detected_emotions:
        detected_emotions = ['neutral']
    
    # Simple sentiment analysis
    positive_words = ['good', 'great', 'awesome', 'love', 'like', 'happy', 'amazing']
    negative_words = ['bad', 'hate', 'terrible', 'awful', 'sad', 'angry']
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        sentiment = 'positive'
    elif neg_count > pos_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    # Generate search keywords
    search_keywords = detected_emotions + [sentiment]
    
    return {
        'top_emotions': detected_emotions[:3],
        'sentiment': sentiment,
        'search_keywords': search_keywords
    }
```
# Enhanced keyword-based text analysis (no AI required)
import re

def analyze_text(text):
    """Enhanced keyword-based text analysis"""
    
    # Comprehensive emotion keywords
    emotion_keywords = {
        'happy': ['happy', 'joy', 'excited', 'cheerful', 'upbeat', 'positive', 'celebrate', 'amazing', 'great', 'wonderful'],
        'sad': ['sad', 'depressed', 'down', 'melancholy', 'blue', 'lonely', 'heartbroken', 'crying', 'miss', 'lost'],
        'angry': ['angry', 'mad', 'furious', 'rage', 'annoyed', 'frustrated', 'hate'],
        'calm': ['calm', 'peaceful', 'relaxed', 'chill', 'serene', 'tranquil', 'zen', 'meditation'],
        'energetic': ['energetic', 'pumped', 'hyped', 'active', 'dynamic', 'workout', 'dance', 'party', 'intense']
    }
    
    text_lower = text.lower()
    detected_emotions = []
    
    # Detect emotions from keywords
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_emotions.append(emotion)
    
    # Enhanced sentiment analysis
    positive_words = ['good', 'great', 'awesome', 'love', 'like', 'happy', 'amazing', 'wonderful', 'fantastic', 'excellent']
    negative_words = ['bad', 'hate', 'terrible', 'awful', 'sad', 'angry', 'worst', 'horrible', 'depressed']
    
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        sentiment = 'positive'
    elif neg_count > pos_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    # Default emotions if none detected
    if not detected_emotions:
        if sentiment == 'positive':
            detected_emotions = ['happy']
        elif sentiment == 'negative':
            detected_emotions = ['sad']
        else:
            detected_emotions = ['neutral']
    
    # Generate search keywords
    search_keywords = detected_emotions + [sentiment]
    
    return {
        'top_emotions': detected_emotions[:3],
        'sentiment': sentiment,
        'search_keywords': search_keywords
    }

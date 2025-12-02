# backend/spotify.py
import requests
import base64
import random

def get_spotify_token(client_id, client_secret):
    """
    Get Spotify API access token
    
    Args:
        client_id (str): Spotify API client ID
        client_secret (str): Spotify API client secret
        
    Returns:
        str: Access token
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    json_result = response.json()
    
    return json_result.get("access_token")

def search_tracks(token, analysis_results):
    """
    Search for tracks based on text analysis results
    
    Args:
        token (str): Spotify API access token
        analysis_results (dict): Results from text analysis
        
    Returns:
        list: Recommended tracks
    """
    base_url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Get search keywords from analysis
    keywords = analysis_results.get("search_keywords", [])
    top_emotions = analysis_results.get("top_emotions", [])
    sentiment = analysis_results.get("sentiment", "neutral")
    
    # If we have too few keywords, add some defaults based on emotions
    if len(keywords) < 2:
        if top_emotions:
            primary_emotion = top_emotions[0]
            if primary_emotion in ["joy", "surprise"]:
                keywords.extend(["happy", "upbeat"])
            elif primary_emotion in ["sadness", "fear"]:
                keywords.extend(["sad", "emotional"])
            elif primary_emotion == "anger":
                keywords.extend(["intense", "powerful"])
            else:
                keywords.extend(["chill", "relaxing"])
    
    # Construct search query
    # We'll do a few different searches and combine results
    all_tracks = []
    
    # Group keywords to create more effective queries
    keyword_groups = []
    
    # Process in pairs if possible
    if len(keywords) >= 2:
        for i in range(0, len(keywords), 2):
            if i+1 < len(keywords):
                keyword_groups.append(f"{keywords[i]} {keywords[i+1]}")
            else:
                keyword_groups.append(keywords[i])
    else:
        keyword_groups = keywords
    
    # Add emotion-specific keywords if we have emotions
    if top_emotions:
        # Add emotion and sentiment to keywords for potential search
        keywords.append(f"{top_emotions[0]} {sentiment}")
    
    # Search for tracks using multiple keyword combinations to get more results
    all_tracks = []
    
    # Create multiple search queries for better coverage
    search_queries = []
    
    # Primary search with main keywords
    primary_query = ' '.join(keywords[:3])
    if primary_query:
        search_queries.append(primary_query)
    
    # Add individual keyword searches for more variety
    for keyword in keywords[:3]:
        if keyword and keyword not in ['neutral', 'positive', 'negative']:  # Skip generic terms
            search_queries.append(keyword)
    
    # Ensure there's at least one query, even if keywords were empty
    if not search_queries and top_emotions:
        search_queries.append(f"{top_emotions[0]} {sentiment}")
    elif not search_queries:
        search_queries.append("mood music") # Fallback if no keywords or emotions
    
    # Limit to prevent too many API calls
    search_queries = list(set(search_queries))[:5] # Remove duplicates and limit queries
    
    # Search with each query
    for query in search_queries:
        params = {
            'q': query,
            'type': 'track',
            'limit': 20,  # Increased from 10 to get more results
            'market': 'US'
        }
        
        response = requests.get(
            f"{SPOTIFY_API_BASE_URL}/search",
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            continue
            
        json_result = response.json()
        if "tracks" in json_result and "items" in json_result["tracks"]:
            all_tracks.extend(json_result["tracks"]["items"])
    
    # Remove duplicates and format results with smart popularity fallback
    unique_track_ids = set()
    
    # Try different popularity thresholds (70 → 60 → 50)
    # Adjusted to get more results while keeping quality
    for min_popularity in [70, 60, 50]:
        recommendations = []
        
        for track in all_tracks:
            # Filter by current popularity threshold
            if track.get("popularity", 0) < min_popularity:
                continue
                
            if track["id"] not in unique_track_ids:
                unique_track_ids.add(track["id"])
                
                # Format track data
                track_data = {
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "preview_url": track["preview_url"],
                    "external_url": track["external_urls"]["spotify"],
                    "image_url": track["album"]["images"][1]["url"] if track["album"]["images"] else None,
                    "uri": track["uri"],
                    "popularity": track.get("popularity", 0)
                }
                recommendations.append(track_data)
        
        # If we found enough songs (at least 8), stop trying lower thresholds
        if len(recommendations) >= 8:
            break
    
    # If still no results, return any songs without popularity filter
    if not recommendations:
        for track in all_tracks:
            if track["id"] not in unique_track_ids:
                unique_track_ids.add(track["id"])
                track_data = {
                    "id": track["id"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "album": track["album"]["name"],
                    "preview_url": track["preview_url"],
                    "external_url": track["external_urls"]["spotify"],
                    "image_url": track["album"]["images"][1]["url"] if track["album"]["images"] else None,
                    "uri": track["uri"],
                    "popularity": track.get("popularity", 0)
                }
                recommendations.append(track_data)
    
    # Sort by popularity (highest first) to get the biggest hits
    recommendations.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Return top 10 most popular tracks
    return recommendations[:10]
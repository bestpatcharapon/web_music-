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
        keyword_groups.append(f"{top_emotions[0]} {sentiment}")
    
    # Limit to prevent too many API calls
    keyword_groups = keyword_groups[:3]
    
    # Execute searches
    for query in keyword_groups:
        params = {
            "q": query,
            "type": "track",
            "limit": 10
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        json_result = response.json()
        
        if "tracks" in json_result and "items" in json_result["tracks"]:
            all_tracks.extend(json_result["tracks"]["items"])
    
    # Remove duplicates and format results
    unique_track_ids = set()
    recommendations = []
    
    for track in all_tracks:
        # Filter by popularity (only megahit songs > 80)
        # This ensures we get songs from top artists like Post Malone, Drake, The Weeknd, etc.
        if track.get("popularity", 0) < 80:
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
    
    # Sort by popularity (highest first) to get the biggest hits
    recommendations.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Return top 10 most popular tracks
    return recommendations[:10]
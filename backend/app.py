# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from model import analyze_text
from spotify import search_tracks, get_spotify_token

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Update CORS for production
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # In production, allow your Vercel domain
    CORS(app, origins=['https://*.vercel.app', 'https://your-app-name.vercel.app'])
else:
    # In development, allow all origins
    CORS(app)

# Initialize Spotify credentials
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

@app.route('/api/recommend', methods=['POST'])
def recommend_songs():
    """Endpoint to recommend songs based on user input text"""
    data = request.json
    user_input = data.get('text', '')
    
    if not user_input:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        # Step 1: Analyze the text using our transformer model
        analysis_results = analyze_text(user_input)
        
        # Step 2: Get access token for Spotify API
        token = get_spotify_token(client_id, client_secret)
        if not token:
            return jsonify({"error": "Failed to authenticate with Spotify API"}), 500
        
        # Step 3: Search for tracks based on analysis
        search_results = search_tracks(token, analysis_results)
        
        # Step 4: Return the recommendations
        return jsonify({
            "analysis": analysis_results,
            "recommendations": search_results
        })
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": "Failed to process request: " + str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # Check if Spotify credentials are set
    if not client_id or not client_secret:
        print("Warning: Spotify credentials not set. Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
    
    # Start the Flask app - Railway will provide PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
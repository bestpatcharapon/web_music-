# Mood to Music - Song Recommendation Website

A web application that recommends songs based on user text input using AI-powered text analysis and the Spotify API.

## Features

- Text analysis using Transformer models to understand user mood and preferences
- Integration with Spotify API to find and recommend relevant songs
- Preview songs directly on the website
- Responsive design that works on desktop and mobile devices

## Project Structure

```
song-recommender/
├── backend/         # Python Flask server
│   ├── app.py        # Main server file
│   ├── model.py      # NLP model handling
│   ├── spotify.py    # Spotify API integration
│   ├── requirements.txt
│   └── .env.example
└── frontend/        # React app
    ├── public/
    ├── src/
    │   ├── App.js
    │   ├── App.css
    │   ├── index.js
    │   └── components/
    │       ├── InputForm.js
    │       └── SongRecommendations.js
    ├── package.json
    └── README.md
```

## Setup Instructions

### Prerequisites

1. Node.js and npm installed
2. Python 3.7+ installed
3. Spotify Developer account

### Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in
2. Create a new app:
   - Click "Create an App"
   - Fill in the app name and description
   - Set the Redirect URI to `http://localhost:3000`
   - Accept the terms and click "Create"
3. On your app's dashboard, note your **Client ID** and **Client Secret**

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd song-recommender/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

5. Edit the `.env` file with your Spotify credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

6. If you're running on a system with limited resources, set `LOW_MEMORY=true` in your `.env` file to use simplified models.

7. Start the Flask server:
   ```bash
   python app.py
   ```
   The server will run on http://localhost:5000

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd song-recommender/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will run on http://localhost:3000

## Usage

1. Open your browser and go to http://localhost:3000
2. Enter text describing how you feel, what music you're looking for, or your current mood
3. Click "Get Song Recommendations"
4. Explore the recommended songs, with the option to preview or open them in Spotify

## How It Works

1. **Text Analysis**: When a user submits text, it's sent to the backend where a transformer model analyzes:
   - Emotions expressed in the text
   - Overall sentiment (positive, negative, neutral)
   - References to specific genres or activities

2. **Keyword Generation**: Based on the analysis, the system generates music-related keywords.

3. **Spotify API Search**: The keywords are used to search for relevant tracks via the Spotify API.

4. **Result Processing**: The search results are processed, duplicates removed, and the top recommendations are returned to the user.

## Troubleshooting

- **Model Loading Issues**: The first request might take longer as the models are loaded.
- **Spotify API Rate Limits**: If you encounter rate limiting, the system will automatically retry after waiting.
- **CORS Issues**: Ensure both servers are running and the CORS settings in the backend are correct.

## Extending the Project

Here are some ideas for extending the project:

1. **User Accounts**: Allow users to save favorite recommendations.
2. **Custom Playlists**: Let users create playlists on Spotify from recommendations.
3. **Fine-tune the Model**: Train a custom model specifically for music recommendation.
4. **Additional Features**: Add mood board visuals, genre filtering, or recommendation history.
5. **Mobile App**: Convert to a Progressive Web App (PWA) or native mobile app.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify API for music data
- Hugging Face Transformers for NLP capabilities
import React, { useState } from 'react';
import './App.css';
import SongRecommendations from './components/SongRecommendations';
import InputForm from './components/InputForm';
import ThemeToggle from './components/ThemeToggle';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState(null);

  // Backend URL - change if your backend is hosted elsewhere
  const BACKEND_URL = 'http://localhost:5000';

  const getRecommendations = async (text) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to get recommendations');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations);
      setAnalysis(data.analysis);
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError(err.message || 'Failed to get recommendations. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="theme-toggle-container">
        <ThemeToggle />
      </div>
      
      <header className="App-header">
        <h1>Mood to Music</h1>
        <p>Tell us how you feel, and we'll recommend the perfect songs for you</p>
      </header>
      
      <main>
        <InputForm onSubmit={getRecommendations} isLoading={isLoading} />
        
        {error && <div className="error-message">{error}</div>}
        
        {analysis && !isLoading && recommendations.length > 0 && (
          <div className="analysis-results">
            <h3>Your Mood Analysis</h3>
            <div className="emotion-tags">
              {analysis.top_emotions.map((emotion, index) => (
                <span key={index} className="emotion-tag">{emotion}</span>
              ))}
              <span className="emotion-tag sentiment">{analysis.sentiment}</span>
            </div>
            <div className="keywords">
              <h4>Search Keywords:</h4>
              <p>{analysis.search_keywords.join(', ')}</p>
            </div>
          </div>
        )}
        
        {isLoading ? (
          <div className="loading">Finding the perfect songs for you...</div>
        ) : (
          <SongRecommendations recommendations={recommendations} />
        )}
      </main>
      
      <footer>
        <p>Built with Spotify API and AI-powered text analysis</p>
      </footer>
    </div>
  );
}

export default App;
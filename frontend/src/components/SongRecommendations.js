import React, { useState } from 'react';

function SongRecommendations({ recommendations }) {
  const [currentlyPlaying, setCurrentlyPlaying] = useState(null);

  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  const togglePlay = (trackId) => {
    if (currentlyPlaying === trackId) {
      setCurrentlyPlaying(null);
    } else {
      setCurrentlyPlaying(trackId);
    }
  };

  return (
    <div className="recommendations-container">
      <h2>Your Recommended Songs</h2>
      {recommendations.length === 0 ? (
        <div className="no-results">
          No songs found. Try a different description!
        </div>
      ) : (
        <div className="song-grid">
          {recommendations.map((track) => (
            <div key={track.id} className="song-card">
              {track.image_url && (
                <div className="song-image">
                  <img src={track.image_url} alt={`${track.name} album cover`} />
                </div>
              )}
              <div className="song-info">
                <h3>{track.name}</h3>
                <p>{track.artist}</p>
                <p className="album-name">{track.album}</p>
              </div>
              <div className="song-actions">
                {track.preview_url ? (
                  <button 
                    className="play-button" 
                    onClick={() => togglePlay(track.id)}
                  >
                    {currentlyPlaying === track.id ? 'Pause' : 'Play Preview'}
                  </button>
                ) : (
                  <a 
                    href={track.external_url} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="play-button external"
                  >
                    Listen on Spotify
                  </a>
                )}
                
                {currentlyPlaying === track.id && track.preview_url && (
                  <audio
                    src={track.preview_url}
                    autoPlay
                    controls
                    onEnded={() => setCurrentlyPlaying(null)}
                  />
                )}
                
                <a 
                  href={track.external_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="spotify-link"
                >
                  Open in Spotify
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SongRecommendations;
import React, { useState } from 'react';

function InputForm({ onSubmit, isLoading }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text);
    }
  };

  const examplePrompts = [
    "I'm feeling really happy today, the sun is shining and I want to celebrate",
    "Need something to help me focus on studying for my exam",
    "I just broke up with my partner and need some comfort music",
    "Looking for energetic workout music for my morning run",
    "I want some calming music to help me sleep tonight",
  ];

  const handleExampleClick = (example) => {
    setText(example);
  };

  return (
    <form onSubmit={handleSubmit} className="input-form">
      <div className="form-control">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe how you're feeling, what's on your mind, or what kind of music you want..."
          rows={4}
          disabled={isLoading}
          required
        />
      </div>
      <button type="submit" disabled={isLoading || !text.trim()}>
        {isLoading ? 'Analyzing...' : 'Get Song Recommendations'}
      </button>
      <div className="examples">
        <p>Try something like:</p>
        <ul>
          {examplePrompts.map((example, index) => (
            <li key={index}>
              <a href="#" onClick={(e) => {
                e.preventDefault();
                handleExampleClick(example);
              }}>{example}</a>
            </li>
          ))}
        </ul>
      </div>
    </form>
  );
}

export default InputForm;
// App.js

import React, { useEffect, useState, useRef } from 'react';
import io from 'socket.io-client';
import './App.css';

const ENDPOINT = 'http://localhost:5000';

function base64ToImage(base64String) {
  const binaryString = atob(base64String);
  const bytes = new Uint8Array(binaryString.length);

  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  const blob = new Blob([bytes], { type: 'image/jpg' });
  const imageUrl = URL.createObjectURL(blob);

  const image = new Image();
  image.src = imageUrl;

  return image;
}

const App = () => {
  const [socket, setSocket] = useState(null);
  const [playerScore, setPlayerScore] = useState(0);
  const [computerScore, setComputerScore] = useState(0);
  const [consecutiveWins, setConsecutiveWins] = useState(0);
  const imageRef = useRef(new Image());
  const [username, setUsername] = useState('');
  const [usernameEntered, setUsernameEntered] = useState(false);
  // Variable for list of top 5 scores
  const [topScores, setTopScores] = useState([]);

  useEffect(() => {
    const socket = io(ENDPOINT);
    setSocket(socket);

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleUsernameSubmit = (e) => {
    e.preventDefault();
    const name = username.trim();
    if (!name) return;
    setUsername(name);
    setUsernameEntered(true);
    socket.emit('username', name);
  };

  useEffect(() => {
    if (!socket) return;

    socket.on('top_scores', (data) => {
      const decoder = new TextDecoder('utf-8');
      setTopScores(data.map((item) => ({ username: decoder.decode(item.username), score: item.score })));
    });

    return () => {
      socket.off('top_scores');
    }
  }, [socket]);

  useEffect(() => {
    if (!socket) return;

    socket.on('video_feed', (frame) => {
      const image = base64ToImage(frame);

      if (!imageRef.current) return;
      imageRef.current.src = image.src;
    });

    return () => {
      socket.off('video_feed');
    }

  }, [socket]);

  // Get scores from server {score, player_score, computer_score}
  useEffect(() => {
    if (!socket) return;

    socket.on('score', (data) => {
      setPlayerScore(data.player_score);
      setComputerScore(data.computer_score);
      setConsecutiveWins(data.consecutive_wins);
    });

    return () => {
      socket.off('score');
    };
  }, [socket]);

  if (!usernameEntered) {
    return (
      <main className="lobby">
        <h1 className="lobby-title">
          <span>Rock</span>
          <span>Paper</span>
          <span>Scissors</span>
        </h1>
        <p className="lobby-sub">Throw your hand at the camera. Best of forever.</p>
        <form className="lobby-form" onSubmit={handleUsernameSubmit}>
          <label htmlFor="username" className="field-label">Your name</label>
          <div className="lobby-row">
            <input
              id="username"
              type="text"
              autoComplete="off"
              autoFocus
              maxLength={20}
              placeholder="e.g. Dustin"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <button type="submit" className="btn btn-primary" disabled={!username.trim() || !socket}>
              Play
            </button>
          </div>
        </form>
      </main>
    );
  }

  return (
    <main className="arena">
      <header className="arena-header">
        <span className="wordmark">Rock Paper Scissors</span>
        <span className={`streak${consecutiveWins > 0 ? ' is-hot' : ''}`}>
          Win streak <strong>{consecutiveWins}</strong>
        </span>
      </header>

      <section className="scoreboard" aria-label="Score">
        <div className="corner corner-red">
          <span className="corner-label">Red corner</span>
          <span className="corner-name">{username}</span>
          <span key={playerScore} className="corner-score">{playerScore}</span>
        </div>
        <span className="vs" aria-hidden="true">vs</span>
        <div className="corner corner-blue">
          <span className="corner-label">Blue corner</span>
          <span className="corner-name">CPU</span>
          <span key={computerScore} className="corner-score">{computerScore}</span>
        </div>
      </section>

      <div className="arena-body">
        <section className="stage">
          <div className="feed">
            <img ref={imageRef} alt="Your webcam feed" />
          </div>
          <div className="controls">
            <button className="btn btn-primary btn-lg" onClick={() => socket.emit('start_game')}>
              Play round
            </button>
            <button className="btn btn-ghost" onClick={() => socket.emit('reset_game')}>
              Reset scores
            </button>
          </div>
        </section>

        <aside className="leaderboard">
          <h2>Best win streaks</h2>
          {topScores.length === 0 ? (
            <p className="empty">No streaks yet. Win a round to get on the board.</p>
          ) : (
            <ol>
              {topScores.map((item) => (
                <li key={item.username} className={item.username === username ? 'is-you' : undefined}>
                  <span className="lb-name">{item.username}</span>
                  <span className="lb-score">{item.score}</span>
                </li>
              ))}
            </ol>
          )}
        </aside>
      </div>
    </main>
  );
};

export default App;

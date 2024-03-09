import React, { useState } from 'react';
import './App.css'; // Include your CSS file for styling

function App() {
  const [step, setStep] = useState(1);
  const [heartRate, setHeartRate] = useState(null);
  const [targetHeartRate, setTargetHeartRate] = useState('');
  const [selectedSong, setSelectedSong] = useState(null);

  const handleSubmitInput = (e) => {
    e.preventDefault();
    // Here you can implement logic to get heart rate data (e.g., from Fitbit)
    // For now, let's simulate heart rate data
    const simulatedHeartRate = Math.floor(Math.random() * (150 - 60 + 1)) + 60; // Random number between 60 and 150
    setHeartRate(simulatedHeartRate);
    setStep(step + 1);
  };

  const handleSubmitTargetHeartRate = (e) => {
    e.preventDefault();
    setStep(step + 1);
    // Here you can implement logic to process the target heart rate input
  };

  const handleSelectSong = () => {
    // Here you can implement logic to select a song based on user's heart rate
    // For now, let's simulate a song selection
    const simulatedSong = {
      title: "Song Title",
      artist: "Artist Name",
      audioUrl: "song.mp3" // Replace with actual URL of the song
    };
    setSelectedSong(simulatedSong);
    setStep(step + 1);
  };

  return (
    <div className="App">
      <header>
        <h1>Placeholder Team Name</h1>
      </header>
      <main>
        {step === 1 && (
          <div>
            <h2>User Input Prompt</h2>
            <form onSubmit={handleSubmitInput}>
              <p>Put on your Fitbit</p>
              <button type="submit">Next</button>
            </form>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong></p>
              </div>
            )}
          </div>
        )}
        {step === 2 && (
          <div>
            <h2>Target Heart Rate</h2>
            <form onSubmit={handleSubmitTargetHeartRate}>
              <label>
                Enter your target heart rate:
                <input
                  type="number"
                  value={targetHeartRate}
                  onChange={(e) => setTargetHeartRate(e.target.value)}
                />
              </label>
              <button type="submit">Next</button>
            </form>
          </div>
        )}
        {step === 3 && (
          <div>
            <h2>Loading...</h2>
            <p>The neural network is selecting a song for you</p>
            {/* You can add a loading animation here if desired */}
            <button onClick={handleSelectSong}>Skip</button>
          </div>
        )}
        {step === 4 && selectedSong && (
          <div>
            <h2>Music</h2>
            <p>Title: {selectedSong.title}</p>
            <p>Artist: {selectedSong.artist}</p>
            <audio controls>
              <source src={selectedSong.audioUrl} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </main>
      <footer>
        <p>Kelly, May, Nipun, and Parthiv for GrizzHacks 2024</p>
      </footer>
    </div>
  );
}

export default App;

"use client"; 

import { useState } from 'react';
import './page.module.css'; // Include your CSS file for styling

export default function Home() {
  const [step, setStep] = useState(1);
  const [heartRateTime, setHeartRateTime] = useState(null)
  const [heartRate, setHeartRate] = useState(null);
  const [targetHeartRate, setTargetHeartRate] = useState('');
  const [selectedSong, setSelectedSong] = useState(null);

  const fetchHeartRateData = async () => {
    try {
      const response = await fetch(
        'https://api.fitbit.com/1/user/-/activities/heart/date/today/today/1min.json',
        {
          headers: {
            Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1JTQ0ciLCJzdWIiOiI2TDZYV1YiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJlY2cgcnNldCByb3h5IHJudXQgcnBybyByc2xlIHJjZiByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNzEwMDUzNDM1LCJpYXQiOjE3MTAwMjQ2MzV9.Vv4jvGSoBHz6fsPR_WhlOXWO6_YnLd8gA0XVTrQ0TW4'
          }
        }
      );
      if (!response.ok) {
        throw new Error('Failed to fetch heart rate data');
      }
      const data = await response.json();
      // Extract heart rate from data
      const mostRecentHeartRate = data["activities-heart-intraday"].dataset.slice(-1)[0];

      // console.log(mostRecentHeartRate)

      setHeartRate(mostRecentHeartRate.value);
      setHeartRateTime(mostRecentHeartRate.time)
      setStep(step + 1);
    } catch (error) {
      console.error('Error fetching heart rate data:', error);
    }
  };

  const handleSubmitInput = (e) => {
    e.preventDefault();
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
              <button type="submit" onClick={fetchHeartRateData}>Next</button>
            </form>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></p>
              </div>
            )}
          </div>
        )}
        
        {step === 2 && (
          <div>
            <h2>Target Heart Rate</h2>
            {heartRate && (
              <div className="heart-rate-display">
                <div className="heart-animation"></div>
                <p>Your heart rate: <strong>{heartRate}</strong> at <strong>{heartRateTime}</strong></p>
              </div>
            )}
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

import librosa

def get_tempo(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    return tempo

def main():
    audio_file = "your_audio_file.wav"  # Replace with the path to your audio file
    tempo = get_tempo(audio_file)

    print(f"Tempo (BPM) of the audio: {tempo}")

if __name__ == "__main__":
    main()

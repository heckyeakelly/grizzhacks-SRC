
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import os
import librosa

#=-=-=-=-=This Section Loads the Neural Network=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# Define the neural network architecture
class MyModel(nn.Module):
    def __init__(self, num_input_variables):
        super(MyModel, self).__init__()
        self.fc = nn.Linear(num_input_variables, 1)

    def forward(self, x):
        return self.fc(x)

# Load the trained model
def load_model(model_path, num_input_variables):
    model = MyModel(num_input_variables)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=USING THE MODEL=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# THIS MODEL TAKES A LIST OF MP3S AND TARGET HEART RATE AND CURRENT HEART RATE FROM JS AND SELECTS A SONG 
# TO GET THE USER TO THEIR TARGET HEART RATE
def useModel(heartRate, targetHeartRate, model_path, musicList, musicdatacsv):
    
    # Get CURRENT User Heart Rate Here (KELLY THIS IS YOUR TIME SO SHINE) DO THIS
    current_heart_rate = heartRate
    
    # INFORMATION ABOUT THE MUSIC GOES IN THIS DATA STRUCTURE HERE:
    musicListInfoDictionaryList = []

    # Path to the trained model file
    model_path = model_path

    # Path to the CSV file containing input and target data
    csv_file_path = musicdatacsv  # Replace with the path to your CSV file

    # Read input data from CSV file to determine the number of input variables
    # We do this because we might want to adjust the size of the model, so simply hardcoding
    # the CSV file of the training data will save us time as we adjust it
    data = pd.read_csv(csv_file_path)
    num_input_variables = len(data.columns) - 1  # Exclude the target variable

    # Load the trained model
    model = load_model(model_path, num_input_variables)

    #Great, now that the model is loaded, it is time to actually use it
    # Create predictions of all heart rates from all files available in the music list
    # based on the current heart rate
    for music_file in musicList: 
        # Get data from the music file using our getdata function
        music_data = getData(music_file)  # Call the getData function
        music_data['heart_rate'] = heartRate  # Add current heart rate to the data
        music_data_tensor = torch.tensor(list(music_data.values()), dtype=torch.float32)  # Convert to tensor
        
        # Append the music data to the master music information list
        with torch.no_grad():
            # Create the predicted heart rate for EVERY music file.
            predicted = model(music_data_tensor.unsqueeze(0))  # Add an extra dimension???
            musicListInfoDictionaryList.append({
                'music_file': music_file,
                'heart_rate_prediction': predicted.item(),
                **music_data  # Include other relevant information about the music file here
            })
    
    # Calculate the change in heart rate per second
    for music_info in musicListInfoDictionaryList:
        music_info['change_in_heart_rate_per_sec'] = calculate_change_in_heart_rate_per_sec(current_heart_rate, music_info['heart_rate_prediction'], music_file_length)
    
    # Select the song that achieves the greatest ABSOLUTE VALUE OF(change in heart rate) that meets the above parameters.
    selected_song = select_song(musicListInfoDictionaryList, current_heart_rate, targetHeartRate)
    
    return selected_song

def calculate_change_in_heart_rate_per_sec(current_heart_rate, predicted_heart_rate, music_file_length):
    # Implement logic to calculate change in heart rate per second
    return abs(predicted_heart_rate - current_heart_rate) / music_file_length

def select_song(musicListInfoDictionaryList, current_heart_rate, target_heart_rate):
    # Implement logic to select the song based on criteria mentioned in comments
    selected_song = None
    max_change_in_heart_rate = -1
    for music_info in musicListInfoDictionaryList:
        if (target_heart_rate >= current_heart_rate and
            current_heart_rate <= music_info['heart_rate_prediction'] < target_heart_rate) or \
           (target_heart_rate < current_heart_rate and
            target_heart_rate <= music_info['heart_rate_prediction'] < current_heart_rate):
            if music_info['change_in_heart_rate_per_sec'] > max_change_in_heart_rate:
                max_change_in_heart_rate = music_info['change_in_heart_rate_per_sec']
                selected_song = music_info['music_file']
    return selected_song

#=-=-= This abomination of a section calculates the data for a given mp3 file=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def get_tempo(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Estimate tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Calculate tempo for the first 30 seconds
    y_first_30 = y[:int(sr * 30)]
    tempo_first_30, _ = librosa.beat.beat_track(y=y_first_30, sr=sr)

    # Calculate tempo for the last 30 seconds
    y_last_30 = y[-int(sr * 30):]
    tempo_last_30, _ = librosa.beat.beat_track(y=y_last_30, sr=sr)

    return tempo, tempo_first_30, tempo_last_30

def get_length(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Calculate duration in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    return duration

def get_avg_pitch(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Compute the pitch
    pitches, _ = librosa.piptrack(y=y, sr=sr)

    # Calculate average pitch over all frames
    avg_pitch = pitches.mean()

    # Calculate average pitch in the first 30 seconds
    avg_pitch_first_30 = pitches[:, :int(sr * 30)].mean()

    # Calculate average pitch in the last 30 seconds
    avg_pitch_last_30 = pitches[:, -int(sr * 30):].mean()

    return avg_pitch, avg_pitch_first_30, avg_pitch_last_30

#This is the function you use.
#It returns a long complicated string that has all the data for a particular mp3 file.
def getData(filepath):
    audio_file = filepath
    tempo, tempo_first_30, tempo_last_30 = get_tempo(audio_file)
    length = get_length(audio_file)
    avg_pitch, pitch_first_30, pitch_last_30 = get_avg_pitch(audio_file)

    print(f"Processing {filepath}...")
    return {
        'file_path': filepath,
        'tempo': tempo,
        'tempo_first_30': tempo_first_30,
        'tempo_last_30': tempo_last_30,
        'length': length,
        'pitch_first_30': pitch_first_30,
        'pitch_last_30': pitch_last_30,
        'avg_pitch': avg_pitch
    }
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


"""
# Example usage
# Assuming appropriate values for the parameters
heartRate = 100
targetHeartRate = 120
model_path = 'trained_model.pth'
musicList = ['song1.mp3', 'song2.mp3']
musicdatacsv = 'music_data.csv'

selected_song = useModel(heartRate, targetHeartRate, model_path, musicList, musicdatacsv)
print("Selected song:", selected_song)
"""
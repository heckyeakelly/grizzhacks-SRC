

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=USING THE MODEL=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# THIS MODEL TAKES A LIST OF MP3S AND TARGET HEART RATE AND CURRENT HEART RATE FROM JS AND SELECTS A SONG 
# TO GET THE USER TO THEIR TARGET HEART RATE
def useModel(heartRate, targetHeartRate, model_path, musicList, musicdatacsv):
    
    import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import os
import librosa

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd



def makeModel(datafilename):
    #=-=-=-==-=-=THIS SECTION CREATES THE MODEL-=-=-=-=-=-=-=-=-=-=-
    # Step 1: Read input data from CSV file
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    #INPUT THE NAME OF YOUR TRAINING DATA CSV
    data = pd.read_csv(datafilename, skiprows=1)  # Replace 'your_data.csv' with the path to your CSV file
    #THE FIRST ROW IS SKIPPED BECAUSE IT IS ASSUMED IT CONTAINS THE NAMES OF THE COLUMNS
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # Extract input variables and target variable from CSV data
    #THESE TWO LINES ARE SUSPECT - MAKE SURE TO EDIT THEM TO REFLECT THAT THE LAST COLUMN OF THE TRAINING DATA IS THE TARGET DATA
    input_data = data.iloc[:, :-1].values.tolist()  # Extract all columns except the last one as input_data
    target_data = data.iloc[:, -1].values.tolist()  #extract ONLY the last column
    #DEBUGGING: MAKE SURE YOUR DATA MATCHES
    print("First row of input_data:")
    print(input_data[0])

    print("First row of target_data:")
    print(target_data[0])


    # Determine the number of input variables BASED ON THE LENGTH OF THE INPUT DATA
    num_input_variables = len(input_data[0])

    # Prepare input and target tensors
    x_train = torch.tensor(input_data, dtype=torch.float32)
    y_train = torch.tensor(target_data, dtype=torch.float32)

    # Step 4: Define the neural network with the appropriate input size
    model = nn.Sequential(
        nn.Linear(num_input_variables, 1)  # Input size determined dynamically, output size 1 for target variable
    )

    # Step 5: Define loss function and optimizer
    criterion = nn.MSELoss()
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #THE LOSS RATE MAY NEED TO CHANGE TO ENSURE THE MODEL CONVERGES ON THE DATA PROPERLY!!!
    optimizer = optim.SGD(model.parameters(), lr=1e-6)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    # Step 6: Training loop
    #YOU MAY HAVE TO CHANGE THE NUMBER OF EPOCHS!!!!
    num_epochs = 10000
    for epoch in range(num_epochs):
        # Forward pass
        outputs = model(x_train)
        loss = criterion(outputs, y_train)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # Access trained model parameters
    trained_model_parameters = model.state_dict()

    # Save the trained model
    torch.save(trained_model_parameters, 'trained_model.pth')
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-
    return model



#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=USING THE MODEL=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# THIS MODEL TAKES A LIST OF MP3S AND TARGET HEART RATE AND CURRENT HEART RATE FROM JS AND SELECTS A SONG 
# TO GET THE USER TO THEIR TARGET HEART RATE
def useModel(heartRate, targetHeartRate, musicList, musicdatacsv):
    
    # Get CURRENT User Heart Rate Here (KELLY THIS IS YOUR TIME SO SHINE) DO THIS
    current_heart_rate = heartRate
    
    # INFORMATION ABOUT THE MUSIC GOES IN THIS DATA STRUCTURE HERE:
    musicListInfoDictionaryList = []



    # Path to the CSV file containing input and target data
    csv_file_path = musicdatacsv  # Replace with the path to your CSV file
    model = makeModel(musicdatacsv)

    #Great, now that the model is loaded, it is time to actually use it
    # Create predictions of all heart rates from all files available in the music list
    # based on the current heart rate
    print("I am working on picking a song from your given music list")
    for music_file in musicList: 
        # Get data from the music file using our getdata function
        music_data = getData(music_file)  # Call the getData function
        print("I am considering ", music_data['file_path'])
        music_data['heart_rate'] = heartRate  # Add current heart rate to the data
        print("I am attempting to create a tensor")
        print(music_data.values())
        music_data_tensor = torch.tensor(list(music_data.values())[1::], dtype=torch.float32)  # Convert to tensor
        
        # Append the music data to the master music information list
        print("Now that I have created a tensor, I am attempting to predict what heart rate it will create")
        with torch.no_grad():
            # Create the predicted heart rate for EVERY music file.
            predicted = model(music_data_tensor.unsqueeze(0))  # Add an extra dimension???
            print("The predicted heart rate is:, ", predicted)
            musicListInfoDictionaryList.append({
                'music_file': music_file,
                'heart_rate_prediction': predicted.item(),
                **music_data  # Include other relevant information about the music file here
            })
    
    print("We have calculated predicted values, it is now to calculate predicted heart rate changes")
    # Calculate the change in heart rate per second
    for music_info in musicListInfoDictionaryList:
        print("Attempting to calculate the change in heart rate per second of: ", music_info['file_path'])
        music_info['change_in_heart_rate_per_sec'] = calculate_change_in_heart_rate_per_sec(current_heart_rate, music_info['heart_rate_prediction'], music_info['length'])
    
    print("We have calculated the change in heart rate, we will now try to select a song")
    # Select the song that achieves the greatest ABSOLUTE VALUE OF(change in heart rate) that meets the above parameters.
    selected_song = select_song(musicListInfoDictionaryList, current_heart_rate, targetHeartRate)
    
    return selected_song

def calculate_change_in_heart_rate_per_sec(current_heart_rate, predicted_heart_rate, music_file_length):
    # Implement logic to calculate change in heart rate per second
    return abs(predicted_heart_rate - current_heart_rate) / music_file_length

def select_song(music_info_list, current_heart_rate, target_heart_rate):
    selected_song = None
    max_change_in_heart_rate = -1

    if current_heart_rate > target_heart_rate:
        # If current heart rate is higher than target
        for music_info in music_info_list:
            if music_info['change_in_heart_rate_per_sec'] < max_change_in_heart_rate or max_change_in_heart_rate == -1:
                max_change_in_heart_rate = music_info['change_in_heart_rate_per_sec']
                selected_song = music_info['music_file']
    else:
        # If current heart rate is lower than or equal to target
        for music_info in music_info_list:
            if music_info['change_in_heart_rate_per_sec'] > max_change_in_heart_rate:
                max_change_in_heart_rate = music_info['change_in_heart_rate_per_sec']
                selected_song = music_info['music_file']
    
    return selected_song


#=-=-= This abomination of a section calculates the data for a given mp3 file=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def get_tempo(audio_file):
    # Load audio file
    print("I am trying to get the tempo of ", audio_file)
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

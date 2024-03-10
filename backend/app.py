from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import UseTheModel
import random

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Define the list of pre-determined MP3 files
MP3_FILES = [
"Baahubali_2_Video_Songs_Telugu_Oka_Pranam_Video_Song_Prabhas_Anushka_Bahubali_Video_Songs.mp3",
"BLACKPINK_-_Kill_This_Love_MV.mp3",
"BTS__Dynamite_Official_MV.mp3"
    # Add remaining files here
]

@app.route('/', methods=['GET'])
def process_heart_rate():
    try:
        # Get heart rate from the query parameters
        heart_rate = int(request.args.get('heartRate'))

        # target heart rate, temporarily hardcoded
        
        target_heart_rate = int(request.args.get('targetHeartRate'))
    

        # For demonstration purposes, let's randomly choose an MP3 file
        selected_mp3 = UseTheModel.useModel(heart_rate, target_heart_rate, './trained_model.pth', MP3_FILES, './Data.csv')

        # Return the selected MP3 file as a response
        return jsonify({'selectedMp3': selected_mp3}), 200
    except ValueError:
        return jsonify({'error': 'Invalid heart rate value. It should be a number.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

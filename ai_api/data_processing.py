import speech_recognition as sr
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
import subprocess

import os
import json
import base64


def encode_image(image_path: str):
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        return None

def ogg_to_text(file_path, model_path='vosk-model-small-ru-0.22'):
    wav_path = os.path.splitext(file_path)[0] + '_temp.wav'
    subprocess.run([
        'ffmpeg',
        '-i', file_path,
        '-ar', '16000',
        '-ac', '1',
        '-y',
        wav_path
    ], check=True, capture_output=True)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)

    try:
        with open(wav_path, 'rb') as f:
            while True:
                data = f.read(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    pass

        result = json.loads(recognizer.FinalResult())
        return result.get('text', 'Речь не распознана')

    except Exception as e:
        return 'None'

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

async def formatting_data(data: str):
    data = data[1:-1]
    data = data.split(',')
    new_data = []
    for el in data:
        new_data.append(el.split(':'))
    try:
        json_data = {
            'name':new_data[0][1].strip(),
            'weight':new_data[1][1].strip(),
            'proteins':new_data[2][1].strip(),
            'calories':new_data[3][1].strip(),
            'fats':new_data[4][1].strip(),
            'carbohydrates':new_data[5][1].strip(),
            'helpfulness':new_data[6][1].strip()
        }
        print(json_data)
        return json_data
    except:
        return False

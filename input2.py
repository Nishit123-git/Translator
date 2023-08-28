import sounddevice as sd
import time
import json
from os.path import join, dirname
import multiprocessing
from scipy.io.wavfile import write
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def callapi():
    authenticator = IAMAuthenticator(apikey)
    global service
    service = SpeechToTextV1(authenticator=authenticator)

    # Insert URL in place of 'API_URL'
    service.set_service_url(
        'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/c834483d-509d-4cd9-b437-06ad0e6a3ac6')
    return service


def record():
    duration = 5.0
    # fs = 440.0
    sps = 48000
    print('recording.....')

    rec = sd.rec(int(duration * sps), samplerate=sps, channels=2)
    sd.wait()
    write('output1.wav', sps, rec)

    print('recording done!')

    with open(join(dirname('__file__'), r'C:\Users\ROHIT\Desktop\machineLearing\trans\output1.wav'),
              'rb') as audio_file:
        dic = json.loads(
            json.dumps(
                service.recognize(
                    audio=audio_file,
                    content_type='audio/wav',  # flac
                    model='en-US_ShortForm_NarrowbandModel',
                    continuous=True).get_result(), indent=2))

    # Stores the transcribed text
    str = ""

    while bool(dic.get('results')):
        str = dic.get('results').pop().get('alternatives').pop().get('transcript') + str[:]

    print(str)

    # Play the waveform out the speakers
    sd.play(rec, sps)
    time.sleep(duration)
    sd.stop()


# porcupine_demo_mic --keywords jarvis
if __name__ == '__main__':
    callapi()
    record()
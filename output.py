from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import wave


# import multiprocessing
def speak(word):
    while True:
        authenticator = IAMAuthenticator(apikey)
        service = TextToSpeechV1(
            authenticator=authenticator
        )
        service.set_service_url(
            'https://api.jp-tok.text-to-speech.watson.cloud.ibm.com/instances/993e1b25-75bd-4c68-ac86-b525349ae6f0')

        with open(join(dirname(__file__), 'output.wav'),
                'wb') as audio_file:
            response = service.synthesize(
                word, accept='audio/wav',
                voice="ko-KR_YoungmiVoice").get_result()
            audio_file.write(response.content)

        class AudioFile:
            chunk = 1024

            def __init__(self, file):
                """ Init audio stream """
                self.wf = wave.open(file, 'rb')
                self.p = pyaudio.PyAudio()
                self.stream = self.p.open(
                    format=self.p.get_format_from_width(self.wf.getsampwidth()),
                    channels=self.wf.getnchannels(),
                    rate=self.wf.getframerate(),
                    output=True
                )

            def play(self):
                """ Play entire file """
                data = self.wf.readframes(self.chunk)
                while data != '':
                    self.stream.write(data)
                    data = self.wf.readframes(self.chunk)

            def close(self):
                """ Graceful shutdown """
                self.stream.close()
                self.p.terminate()

        # Usage example for pyaudio
        a = AudioFile("output.wav")
        a.play()
        a.close()
        break
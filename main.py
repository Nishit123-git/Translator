import json
from os.path import join, dirname
import output
from ibm_watson import SpeechToTextV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator




def translate():
    # Insert API Key in place of
    # 'YOUR UNIQUE API KEY'
    authenticator = IAMAuthenticator(API_key)
    service = SpeechToTextV1(authenticator=authenticator)

    # Insert URL in place of 'API_URL'
    service.set_service_url(
        'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/c834483d-509d-4cd9-b437-06ad0e6a3ac6')

    authenticator1 = IAMAuthenticator(apikey)
    language_translator = LanguageTranslatorV3(
        version='2018-05-01',
        authenticator=authenticator1
    )
    language_translator.set_service_url(
        'https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/40a5d61f-cb0b-4e9b-b1ed-c0eb2a240b9d')
    with open(join(dirname('__file__'), r'C:\Users\ROHIT\Desktop\machineLearing\trans\output.wav'),
              'rb') as audio_file:
        dic = json.loads(
            json.dumps(
                service.recognize(
                    audio=audio_file,
                    content_type='audio/wav',  # flac
                    model='en-US_NarrowbandModel',
                    continuous=True).get_result(), indent=2))

    # Stores the transcribed text
    str = ""

    while bool(dic.get('results')):
        str = dic.get('results').pop().get('alternatives').pop().get('transcript') + str[:]

    print(str)
    trans = language_translator.translate(text=str, model_id='en-ko').get_result()
    trans = trans['translations'][0]['translation']
    print(trans)
    output.speak(trans)


if __name__ == '__main__':
    translate()

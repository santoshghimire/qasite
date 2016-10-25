import pydub
from watson_developer_cloud import TextToSpeechV1


def convert_tts(text, file_path, mp3_file_path):
    """
    Convert given text to speech audio file.
    """
    text_to_speech = TextToSpeechV1(
        username='IBMWATSON_USERNAME',
        password='IBMWATSON_PASSWORD')
    voice = 'en-US_AllisonVoice'
    accept = 'audio/wav'

    with open(file_path, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(text, voice=voice, accept=accept)
        )

    mp3_ver = pydub.AudioSegment.from_wav(file_path)
    mp3_ver.export(mp3_file_path, format="mp3")

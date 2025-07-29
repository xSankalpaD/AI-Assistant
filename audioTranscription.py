import speech_recognition as sr


def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  # Capture the audio from  file
    try:
        text = recognizer.recognize_google(audio)  # Google's speech recognition API
        print(f"Transcription: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Transcribe audio and use the text
audio_file = "./assets/harvard.wav"  
transcript = transcribe_audio(audio_file)
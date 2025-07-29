import whisper

# Load whisper model
def whisper_model(audio):
    model = whisper.load_model("base")  #small, medium, large
 

    result = model.transcribe(audio)  #mp3 works too i think
    
    

    transcript = result["text"]
    
    print("Transcription completed:\n", transcript)

    return transcript





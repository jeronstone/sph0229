import whisper

model = whisper.load_model("small")
result = model.transcribe("testing.wav")
print(result["text"])
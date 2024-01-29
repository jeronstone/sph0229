import whisper
import subprocess
import sys

print("----------")
print(sys.argv)
p = sys.argv[1]

command = "ffmpeg -i ~/exit_int_venv/P" + str(p) + ".AVI -ab 160k -ac 2 -ar 44100 -vn audioP" + str(p) + ".wav"

subprocess.call(command, shell=True)

print("start P " + str(p))
model = whisper.load_model("medium")
result = model.transcribe("audioP" + str(p) + ".wav")
print(result["text"])

f = open("raw+transcript_P" + str(p) + ".txt", "w")
f.write(result["text"])
f.close()

print("end P " + str(p))
print("----------")
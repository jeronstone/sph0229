# Exit Interview Proessing (speech to text) with whisper

Note: any command with `python` may need to be `python3` instead

## Setting up Venv

Clone this repo, then:    
```python -m venv /path/to/new/virtual/environment```     
```source bin/activate/``` (use this command to reactivate venv later - other commands only need to be run on first activation)     
```sudo apt-get update```     
```sudo apt update && sudo apt install ffmpeg```     
```pip install -r requirements.txt```     

Use ```deactivate``` to exit venv

## Running speech to text on exit interviews

1. Place the .AVI file in the venv directory
2. Rename the file to be in the format: P##.AVI (example: P21.AVI, P30.AVI, P36.AVI, etc.)
3. ```python textify.py ## ## ...``` (examples: ```python textify.py 25``` will run the speech to text on `P25.AVI` ' ```python textify.py 26 27``` will run the speech to text on `P26.AVI` AND `P27.AVI`) You can add as many arguments as needed. There is no error checking though, so don't mess up.

At this point, there should be a `.wav` file of the audio, and a `.txt` file with the script. From there, listen to the `.wav` file and make necessary edits to the `.txt` file - the AI isn't perfect.

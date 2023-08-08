"""subtitles.py"""

import pathlib
import whisper
import librosa
import soundfile as sf
from datetime import timedelta

def transcribe_audio(filepath: pathlib.Path) -> dict:
  model = whisper.load_model("base") # Change this to your desired model
  return model.transcribe(audio=filepath, fp16=False)


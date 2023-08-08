"""subtitles.py"""

import pathlib
import whisper
import librosa
import soundfile as sf
from datetime import timedelta

def transcribe_audio(filepath: pathlib.Path) -> dict:
  model = whisper.load_model("base") # Change this to your desired model
  return model.transcribe(audio=filepath, fp16=False)

def format_as_srt(transcription: dict, outfile = None) -> None:
  """..."""
  all_segments = []

  for segment in transcription['segments']:
    startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
    endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
    text = segment['text']
    segmentId = segment['id']+1
    segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}"
    all_segments.append(segment)

  if outfile is not None:
    assert outfile.endswith('.srt')
    with open(outfile, 'w', encoding='utf-8') as srt_file:
      srt_file_contents = '\n\n'.join(all_segments)
      srt_file.write(srt_file_contents)

  return all_segments
"""subtitles.py"""

import pathlib
import whisper
import librosa
import soundfile as sf
from datetime import timedelta
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Bar:
  """a timestamped line of lyrics"""
  text: str
  timestamp: float

@dataclass
class Lyrics:
  """audio transcriptions with timestamps"""

  segments: List[Dict] 

  def get_bars(self) -> List[Bar]:
    """..."""
    bars = []
    for segment in self.segments:
      line_of_lyrics = segment['text'].strip()
      timestamp = segment['start']
      bars.append(Bar(line_of_lyrics, timestamp))
    return bars

  def get_plaintext(self) -> str:
    """
    returns all lyrics as a single string
    """ 
    return '\n'.join(bar.text for bar in self.get_bars())

  def save_as_srt(self, outfile):
    """
    saves each bar and its timestamp and saves it to a SRT file (standard transcription format)
    """
    formatted_segments = []
    for segment in self.segments:
      startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
      endTime = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
      text = segment['text']
      segmentId = segment['id']+1
      segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}"
      formatted_segments.append(segment)

    assert outfile.endswith('.srt')
    with open(outfile, 'w', encoding='utf-8') as srt_file:
      srt_file_contents = '\n\n'.join(formatted_segments)
      srt_file.write(srt_file_contents)

    return formatted_segments

  @classmethod
  def load(Cls, filepath: pathlib.Path):
    """
    uses the whisper library to generate timestamped lyrics from audio 
    """
    model = whisper.load_model("base")
    segments = model.transcribe(audio=filepath, fp16=False)['segments']
    return Cls(segments)

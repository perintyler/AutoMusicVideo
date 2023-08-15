"""subtitles.py"""

import pathlib
import json
import whisper
import librosa
import soundfile as sf
from datetime import timedelta
from typing import List, Dict
from dataclasses import dataclass, asdict

@dataclass
class Bar:
  """a timestamped line of lyrics"""

  text: str
  line_number: int
  start_time: float
  end_time: float

  def as_dict(self):
    return {
      'text': self.text,
      'line_number': self.line_number,
      'start_time': self.start_time,
      'end_time': self.end_time,
    }

  def get_duration(self):
    """returns the amount of time elapsed (in seconds) between the start and end of the bar
    """
    return self.end_time - self.start_time

  @classmethod
  def from_json(Cls, json_bar):
    """"""
    text = json_bar['text']
    line_number = json_bar['line_number'] if 'line_number' in json_bar else json_bar['id']+1
    start_time = json_bar['start_time'] if 'start_time' in json_bar else json_bar['start']
    end_time = json_bar['end_time'] if 'end_time' in json_bar else json_bar['end']
    return Cls(text.strip(), line_number, start_time, end_time)

@dataclass
class Lyrics:
  """audio transcriptions with timestamps"""

  bars: List[Bar]
  source_file: str

  def get_plaintext(self) -> str:
    """returns all lyrics as a single string
    """ 
    return '\n'.join(bar.text for bar in self.bars)

  def save_as_srt(self, outfile):
    """saves each bar and its timestamp and saves it to a SRT file (standard transcription format)
    """
    assert outfile.endswith('.srt')

    srt_sections = []

    for bar in self.bars:
      start_time_string = f'0{timedelta(seconds=int(bar.start_time))},000'
      end_time_string = f'0{timedelta(seconds=int(bar.end_time))},000'
      srt_sections.append(f"{bar.line_number}\n{start_time_string} --> {end_time_string}\n{bar.text.strip()}")

    srt_file_contents = '\n\n'.join(srt_sections)

    with open(outfile, 'w', encoding='utf-8') as srt_file:
      srt_file.write(srt_file_contents)

    return srt_file_contents

  def as_dict(self) -> dict:
    """serializes all encapsulated data, which can be used to re-create instances of `Lyrics` later on
    """
    return {
      'bars': [bar.as_dict() for bar in self.bars],
      'source_file': self.source_file, 
    }

  # def save_as_json(self, outfile):
  #   """
  #   writes all encapsulated data to a JSON file, which can be loaded from file later on with `load_from_json`
  #   """
  #   assert outfile.endswith('.json')
  #   json_contents = self.as_dict()

  #   with open(outfile, 'w') as lyrics_json_file:
  #     json.dump(json_contents, lyrics_json_file)

  #   return json_contents

  # @classmethod
  # def load_from_json(Cls, filepath):
  #   """
  #   creates a new instance of `Lyrics` using a JSON file created by the `save_as_json` function
  #   """
  #   with open(filepath, 'r') as lyrics_json_file:
  #     json_contents = json.load(lyrics_json_file)

  #   source_file = json_contents['source_file']
  #   bars = [Bar.from_json(bar_json) for bar_json in json_contents['bars']]

  #   return Cls(bars, source_file)

  @classmethod
  def load_from_audio(Cls, filepath):
    """
    creates a new instance of `Lyrics` by transcribing lyrics with OpenAI's whisper library 
    """
    source_file = filepath
    model = whisper.load_model("base")

    transcription = model.transcribe(audio=filepath, fp16=False)
    bars = [Bar.from_json(segment) for segment in transcription['segments']]

    return Cls(bars, source_file)

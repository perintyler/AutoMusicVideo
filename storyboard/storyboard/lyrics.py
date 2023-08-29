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
class Lyric:
  """a timestamped lyric from a song
  """

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
    """returns the amount of time elapsed (in seconds) between the start and end of the lyric
    """
    return self.end_time - self.start_time

  @classmethod
  def from_json(Cls, json_lyric):
    """"""
    text = json_lyric['text'].strip()
    line_number = int(json_lyric['line_number'])
    start_time = float(json_lyric['start_time'])
    end_time = float(json_lyric['end_time'])
    return Cls(text, line_number, start_time, end_time)

  @staticmethod
  def save_as_srt(lyrics: List['Lyric'], outfile=None) -> str:
    """saves each lyric and its timestamp and saves it to a SRT file (standard transcription format)
    """
    srt_sections = []

    for lyric in lyrics:
      start_time_string = f'0{timedelta(seconds=int(lyric.start_time))},000'
      end_time_string = f'0{timedelta(seconds=int(lyric.end_time))},000'
      srt_sections.append(f"{lyric.line_number}\n{start_time_string} --> {end_time_string}\n{lyric.text.strip()}")

    srt_file_contents = '\n\n'.join(srt_sections)

    if outfile is not None:
      with open(outfile, 'w', encoding='utf-8') as srt_file:
        assert outfile.endswith('.srt')
        srt_file.write(srt_file_contents)

    return srt_file_contents

  @classmethod
  def load_all_from_audio(Cls, filepath) -> List['Lyric']:
    """transcribes lyrics with OpenAI's whisper library 
    """
    transcription_model = whisper.load_model("base")
    transcription = transcription_model.transcribe(audio=filepath, fp16=False)

    lyrics = []
    for segment in transcription['segments']:
      text = segment['text'].strip()
      line_number = int(segment['id'])+1
      start_time = float(segment['start'])
      end_time = float(segment['end'])
      lyrics.append(Cls(text, line_number, start_time, end_time))

    return lyrics

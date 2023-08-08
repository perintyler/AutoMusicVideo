"""audio.py"""

import librosa
import pathlib
from dataclasses import dataclass
from typing import List

@dataclass
class Audio:
  waveform: List[float]
  samplerate: int

  @classmethod
  def load(Cls, filepath: pathlib.Path):
    """..."""
    waveform, samplerate = librosa.load(filepath)
    return Cls(waveform, samplerate)

"""audio.py"""

import librosa
import pathlib
from dataclasses import dataclass
from typing import List

@dataclass
class Audio:
  waveform: List[float]
  samplerate: int
  filepath: str = None

  def save_as_wav(self, outfile, normalize_audio = False):
    """
    writes the waveform to a WAV file
    """
    librosa.output.write_wav(self.waveform, self.samplerate, normalize = normalize_audio)

  @classmethod
  def load(Cls, filepath: pathlib.Path):
    """..."""
    waveform, samplerate = librosa.load(filepath)
    return Cls(waveform, samplerate, filepath=filepath)

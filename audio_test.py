
from audio import Audio
import numpy as np

def test_load_audio():
  audio = Audio.load('test-data/something-beatles_verse1.wav')
  assert audio.waveform is not None
  assert type(audio.waveform) is np.ndarray
  assert len(audio.waveform) > 0
  assert audio.samplerate is not None
  assert type(audio.samplerate) is int
  assert audio.samplerate > 0

from audio import Audio
import numpy as np

def test_load_audio():
  path_to_test_file = 'test-data/audio/something-beatles_verse1.wav'
  audio = Audio.load(path_to_test_file)
  assert audio.waveform is not None
  assert type(audio.waveform) is np.ndarray
  assert len(audio.waveform) > 0
  assert audio.samplerate is not None
  assert type(audio.samplerate) is int
  assert audio.samplerate > 0
  assert audio.filepath == path_to_test_file
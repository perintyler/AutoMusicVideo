"""isolate_vocals_test.py"""

import os
from audio import Audio
from isolate_vocals import isolate_vocals

def test_isolate_vocals():
  audio = Audio.load('test-data/something-beatles_verse1.wav')
  outfile = '/tmp/isolated-vocals-test.wav'
  isolate_vocals(audio, outfile)
  assert os.path.exists(outfile)

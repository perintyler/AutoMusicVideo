"""subtitles_test.py"""

import pathlib
import os
from .lyrics import Lyrics

lyrics1 = Lyrics.load_from_audio('test-data/audio/something-beatles_verse1.wav')

def test_get_bars():
  assert [bar.text for bar in lyrics1.bars] == [
    "Something in the way she moves attracts me like no other lover",
    "Something in the way she moves me"
  ]

def test_get_lyrics():
  assert lyrics1.get_plaintext() == \
"""Something in the way she moves attracts me like no other lover
Something in the way she moves me"""

def test_srt_file_generation():
  srt_filepath = '/tmp/subtitle-test.srt'
  lyrics1.save_as_srt(outfile=srt_filepath)
  assert os.path.exists(srt_filepath)
  with open(srt_filepath) as srt_file:
    assert srt_file.read() == \
"""1
00:00:00,000 --> 00:00:19,000
Something in the way she moves attracts me like no other lover

2
00:00:19,000 --> 00:00:26,000
Something in the way she moves me"""


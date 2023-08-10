"""subtitles_test.py"""

import pathlib
import os
from transcriptions import Transcription

transcription1 = Transcription.load('test-data/audio/something-beatles_verse1.wav')

def test_get_bars():
  assert transcription1.get_bars() == [
    "Something in the way she moves attracts me like no other lover",
    "Something in the way she moves me"
  ]

def test_get_lyrics():
  assert transcription1.get_lyrics() \
      == "Something in the way she moves attracts me like no other lover\nSomething in the way she moves me"

def test_srt_file_generation():
  srt_filepath = '/tmp/subtitle-test.srt'
  transcription1.save_as_srt(outfile=srt_filepath)
  assert os.path.exists(srt_filepath)
  with open(srt_filepath) as srt_file:
    assert srt_file.read() == \
"""1
00:00:00,000 --> 00:00:19,000
Something in the way she moves attracts me like no other lover

2
00:00:19,000 --> 00:00:26,000
Something in the way she moves me"""

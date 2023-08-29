"""subtitles_test.py"""

import pathlib
from importlib.resources import files
import os
from .lyrics import Lyric

path_to_test_audio = files('storyboard.data').joinpath('something-beatles_verse1.mp3')
test_lyrics = Lyric.load_all_from_audio(str(path_to_test_audio))

def test_load_lyrics_from_audio():
  assert [lyric.text for lyric in test_lyrics] == [
    "Something in the way she moves attracts me like no other lover",
    "Something in the way she moves me"
  ]
  assert [lyric.line_number for lyric in test_lyrics] == [1, 2]

def test_srt_file_generation():
  srt_filepath = '/tmp/subtitle-test.srt'
  expected = \
"""1
00:00:00,000 --> 00:00:19,000
Something in the way she moves attracts me like no other lover

2
00:00:19,000 --> 00:00:26,000
Something in the way she moves me"""

  assert Lyric.save_as_srt(test_lyrics, outfile=srt_filepath) == expected
  assert os.path.exists(srt_filepath)
  with open(srt_filepath) as srt_file:
    assert srt_file.read() == expected

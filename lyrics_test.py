"""subtitles_test.py"""

import pathlib
import os
from lyrics import Lyrics

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

def test_save_and_load_lyrics_from_json():
  json_file_path = '/tmp/lyrics-save-and-load-test.json'
  lyrics1.save_as_json(json_file_path)
  loaded_lyrics = Lyrics.load_from_json(json_file_path)
  assert lyrics1.source_file == loaded_lyrics.source_file
  for original_bar, loaded_bar in zip(lyrics1.bars, loaded_lyrics.bars):
    assert original_bar.text == loaded_bar.text
    assert original_bar.line_number == loaded_bar.line_number
    assert original_bar.start_time == loaded_bar.start_time
    assert original_bar.end_time == loaded_bar.end_time


"""subtitles_test.py"""

import pathlib
import os
import subtitles

def test_transcribe_something_by_beatles():
  # test transcriptions
  testfile = 'test-data/something-beatles_verse1.wav'
  transcription = subtitles.transcribe_audio(testfile)
  lyrics = ' '.join(segment['text'].strip() for segment in transcription['segments'])
  assert lyrics == "Something in the way she moves attracts me like no other lover Something in the way she moves me"

  # test srt file generation
  srt_filepath = '/tmp/subtitle-test.srt'
  srt_segments = subtitles.format_as_srt(transcription, outfile=srt_filepath)
  assert srt_segments is not None
  assert type(srt_segments) is list
  assert len(srt_segments) > 0
  for segment in srt_segments:
    assert type(segment) is str
    assert len(segment) > 0
  assert os.path.exists(srt_filepath)

  with open(srt_filepath) as srt_file:
    assert srt_file.read() == '\n\n'.join(srt_segments)



from importlib.resources import files
from .audio import Audio
from .beats import Beats

test_audio_file = files('editing_room.test_audio').joinpath('piano-clip.mp3')

expected_timestamp = [
  0.053, 0.992, 1.952, 2.987, 3.883, 4.843, 5.803, 6.741, 7.648, 8.501, 9.355, 10.176, 11.008, 11.925
]

def test_load_beats():
  beats = Beats.load(Audio.load(test_audio_file))

  assert len(beats.timestamps) == len(expected_timestamp)

  for actual, expected in zip(beats.timestamps, expected_timestamp):
    assert actual == expected

def test_get_closes_beat():
  beats = Beats.load(Audio.load(test_audio_file))
  assert beats.get_closest(-4.2) == expected_timestamp[0]
  assert beats.get_closest(1.03) == expected_timestamp[1]
  assert beats.get_closest(1.6) == expected_timestamp[2]
  assert beats.get_closest(13.2) == expected_timestamp[-1]

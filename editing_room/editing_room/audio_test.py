"""Test File: AutoMusicVideo::editing_room.audio_test"""

import os
from importlib.resources import files
from moviepy.editor import VideoClip
import numpy as np
from pytest import approx
from .audio import Audio

test_audio_file = files('editing_room.test_audio').joinpath('something-beatles_verse1.mp3')
test_gif = files('editing_room.test_gifs').joinpath('test1.gif')

def test_load_audio():
  audio = Audio.load(test_audio_file)
  assert audio.waveform is not None
  assert type(audio.waveform) is np.ndarray
  assert len(audio.waveform) > 0
  assert audio.samplerate is not None
  assert type(audio.samplerate) is int
  assert audio.samplerate > 0
  assert str(audio.path) == str(test_audio_file)
  assert audio.duration == approx(26.388)
  assert audio.num_channels == 2

def test_download_audio():
  audio = Audio.download('test-song')
  assert audio.duration == 17.0
  assert audio.num_channels == 2
  assert str(audio.path.stem) == 'test-song'

def test_attach_audio():
  audio = Audio.load(test_audio_file)
  video_clip = VideoClip(lambda t: np.zeros((1280, 720, 3), dtype=np.uint8), duration=5)
  audio.attach_to(video_clip)
  assert video_clip.audio is not None
  assert video_clip.audio.duration == video_clip.duration
  assert video_clip.audio.fps == audio.samplerate
  assert video_clip.audio.nchannels == audio.num_channels

def test_audio_to_mono():
  stereo_audio = Audio.load(test_audio_file)
  assert stereo_audio.is_stereo()
  mono_audio = stereo_audio.as_mono()
  assert mono_audio.is_mono()
  assert mono_audio.num_channels == 1
  assert stereo_audio.num_samples == mono_audio.num_samples
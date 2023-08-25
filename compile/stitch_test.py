"""stitch_test.py"""

import os

import moviepy.editor as mp

from audio import Audio
from stitch import create_video_from_gifs, attach_audio_to_video

def test_create_video_from_gifs():
  paths_to_gifs = [f'test-data/gifs/test{i}.gif' for i in (1,2,3)]
  path_to_video = '/tmp/create-video-from-gifs-test.mp4'
  clip = create_video_from_gifs(paths_to_gifs, outfile=path_to_video)
  assert os.path.exists(path_to_video)
  assert clip.duration == 3.75

def test_attach_audio_to_video():
  path_to_audio = 'test-data/audio/something-beatles_verse1.mp3'
  video = mp.VideoFileClip('test-data/video/test1.mp4').without_audio()  
  attach_audio_to_video(path_to_audio, video)
  assert video.audio is not None
  assert isinstance(video.audio, mp.AudioClip)
  assert video.audio.duration == 6.9
  
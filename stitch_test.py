"""stitch_test.py"""

import os

from stitch import create_video_from_gifs

def test_create_video_from_gifs():
  paths_to_gifs = [f'test-data/gifs/test{i}.gif' for i in (1,2,3)]
  path_to_video = '/tmp/create-video-from-gifs-test.mp4'
  clip = create_video_from_gifs(paths_to_gifs, outfile=path_to_video)
  assert os.path.exists(path_to_video)
  assert clip.duration == 3.75

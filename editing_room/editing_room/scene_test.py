"""Test File: AutoMusicVideo::editing_room.scene_test"""

from importlib.resources import files
from .audio import Audio
from .beats import Beats

scenes = []

def test_create_all_scenes():
  audio = Audio.load(files('editing_room.test_audio').joinpath('piano-clip.mp3'))
  chapters = None
  beats = None

  for chapter, scene in Scene.create_all(audio, chapters, beats):
    assert scene.duration > 0
    assert scene.chapter == chapter
    scenes.append(scene)

def test_scene_as_clip():
  pass

def test_scene():
  

  def test_create_scenes():
    pass

  def test_scene_duration():
    pass

  def test_scene_as_clip():
    pass

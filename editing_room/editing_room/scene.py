"""AutoMusicVideo.editing.scene"""

from typing import List
from dataclasses import dataclass

from PIL import Image
from numpy import asarray
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, concatenate_videoclips
import storyboard

from .beats import Beats
from .audio import Audio

FRAMES_PER_SECOND = 24

LYRICS_POSITION = ("center", "bottom")

@dataclass
class Scene:
  """
  """

  chapter: storyboard.Chapter
  start_time: float
  end_time: float

  @property
  def duration(self) -> float:
    """
    note: this is different than chapter duration, since the scene will start and end in 
    sync with the audio, not neccessarily when the chapter's lyric starts or ends
    """
    return self.end_time - self.start_time

  def as_clip(self, overlay_lyrics = True):
    """
    combines the chapter's content (i.e. images) into a video clip, which should show the 
    text to image model thought process as it "draws" to fit the prompt (i.e. lyrics)
    """
    subclip_duration = self.duration / self.chapter.num_content_files()

    subclips = []

    for image_bytes in self.chapter.generate_content():
      image = Image.open(image_bytes)
      image_array = asarray(image)
      image_clip = ImageClip(image_array, duration=subclip_duration)
      subclips.append(image_clip)

    scene_clip = concatenate_videoclips(subclips)

    if overlay_lyrics:
      lyrics_clip = TextClip(lyric, fontsize=24, color="gray")
      lyrics_clip.set_duration(duration)
      lyrics_clip = lyrics_clip.set_position(LYRICS_POSITION)
      scene_clip = CompositeVideoClip([scene_clip, lyrics_clip])

    return kareoke_clip

  @classmethod
  def create_all(Cls, audio: Audio, chapters: storyboard.Chapter, beats: Beats):
    """
    creates a scene for each chapter where transitions occur in sync with the song  
    """
    assert len(chapters) > 0

    scenes = []
    for chapter in chapters:
      start_time = 0.0 if chapter.number == 1 else scenes[-1].end_time
      end_time = beats.get_closest(chapter.lyric.end_time)
      scenes.append(Cls(chapter, start_time, end_time))

    scenes[-1].end_time = audio.duration # make the last scene end at the end of the video

    return scenes

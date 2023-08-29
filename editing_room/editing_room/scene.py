"""AutoMusicVideo.editing.scene"""

from typing import List
from dataclasses import dataclass

import moviepy.editor as mp
import storyboard

from .beats import Beats

@dataclass
class Scene:
  """
  """

  chapter: storyboard.Chapter
  start_time: float
  end_time: float

  @property
  def duration(self):
    """
    note: this is different than chapter duration, since the scene will start and end in 
    sync with the audio, not neccessarily when the chapter's lyric starts or ends
    """
    return self.end_time - self.start_time

  def as_clip(self):
    """
    combines the chapter's content (i.e. images) into a video clip, which should show the 
    text to image model thought process as it "draws" to fit the prompt (i.e. lyrics)
    """
    image_clip_duration = self.duration / chapter.num_content_files()

    subclips = []
    for image_bytes in chapter.generate_content():
      subclips.append(
        mp.ImageClip(image_bytes).set_duration(image_clip_duration)
      )

    return mp.concatenate_videoclips(clips, method="compose")

  @classmethod
  def create_all(Cls, chapters: storyboard.Chapter, beats: Beats):
    """
    creates a scene for each chapter where transitions occur in sync with the song  
    """
    scenes = []
    for chapter in chapters:
      start_time = 0.0 if chapter.number == 1 else scenes[-1].end_time
      end_time = beats.get_closest(chapter.lyric.end_time)
      scenes.append(Cls(chapter, start_time, end_time))

    return scenes

    # for beat_index in range(len(beat_timestamps-1)):
    #   early_beat_timestamp = beat_timestamps[beat_index]
    #   late_beat_timestamp = beat_timestamps[beat_index+1]
    #   scene_index = len(scenes)
    #   chapter_end_time = chapters[scene_index].end_time
    #   if chapter_end_time > early_beat_timestamp and chapter_end_time < late_beat_timestamp:
    #     time_since_last_beat = chapter_end_time - beat_timestamps[beat_index]
    #     time_until_next_beat = late_beat_timestamp - chapter_end_time
    #     transition_timestamp = early_beat_timestamp if time_since_last_beat < time_until_next_beat else late_beat_timestamp
    #     previous_transition_timestamp = scenes[-1].end_time if len(scenes) > 0 else 0.0
    #     scenes.append(Cls(chapter, previous_transition_timestamp, transition_timestamp))

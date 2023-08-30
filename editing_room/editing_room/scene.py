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

OVERLAY_LYRICS = True

SAVE_SCENES_LOCALLY = True

KAREOKE = False

LYRICS_POSITION = ("center", "bottom")

def get_karaoke_clip(video_clip, lyrics):
  lyrics_clip = TextClip(lyrics, fontsize=24, color="gray")
  lyrics_clip.set_duration(video_clip.duration)
  lyrics_clip = lyrics_clip.set_position(LYRICS_POSITION)
  return CompositeVideoClip([video_clip, lyrics_clip])

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

  def as_clip(self):
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

    if KAREOKE:
      scene_clip = get_karaoke_clip(scene_clip, self.chapter.lyric.text)

    if SAVE_SCENES_LOCALLY:
      kareoke_clip.write_videofile(
        f'scene-{self.chapter.number}.mp4', 
        codec='libx264', audio_codec='aac', fps=FRAMES_PER_SECOND
      )

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

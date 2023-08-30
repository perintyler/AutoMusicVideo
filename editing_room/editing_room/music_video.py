"""AutoMusicVideo::editing_room.music_video"""

from io import BytesIO
from typing import List
from dataclasses import dataclass

from moviepy.editor import VideoClip, concatenate_videoclips

from .audio import Audio
from .beats import Beats
from .scene import Scene

import storyboard

FRAMES_PER_SECOND = 24

@dataclass
class MusicVideo:

  song_id: str
  scenes: List[Scene]
  audio: Audio
  beats: Beats

  def as_clip(self) -> VideoClip:
    """
    compiles and concatenates each scene into one video with the song as audio
    """
    scene_clips = [scene.as_clip() for scene in self.scenes]
    combined_scenes = concatenate_videoclips(scene_clips, method='compose')
    return self.audio.attach_to(combined_scenes)

  def as_bytes(self) -> BytesIO:
    video_buffer = BytesIO()
    self.as_clip().write_videofile(video_buffer, codec='libx264', audio_codec='aac', fps=FRAMES_PER_SECOND)
    video_bytes = video_buffer.getvalue()
    video_buffer.close()
    return video_bytes

  def save(self, outfile) -> VideoClip:
    """
    """
    video_clip = self.as_clip()
    video_clip.write_videofile(outfile, codec='libx264', audio_codec='aac', fps=FRAMES_PER_SECOND)
    return video_clip

  def upload(self):
    """
    uploads an mp4 to the cloud storage bucket
    """
    storyboard.cloud_storage.outputs.upload_video(self.song_id, self.as_bytes())

  @classmethod
  def create_new(Cls, song_id):
    """
    downloads the audio and chapters for the given song id and returns a new `MusicVideo` object
    """
    audio = Audio.download(song_id)
    chapters = storyboard.get_chapters(song_id)
    beats = Beats.load(audio.as_mono())
    scenes = Scene.create_all(audio, chapters, beats)
    return Cls(song_id, scenes, audio, beats)

if __name__ == '__main__':
  music_video = MusicVideo.create_new('test-song')
  music_video.save('music-video.mp4')
  music_video.upload()
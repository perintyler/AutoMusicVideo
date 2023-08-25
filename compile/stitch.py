"""stitch.py"""

import librosa

import moviepy.editor as mp
from audio import Audio

def create_video_from_gifs(infiles, outfile = None, gif_duration = None) -> mp.VideoFileClip:
  gif_clips = [mp.VideoFileClip(path_to_gif) for path_to_gif in infiles]

  if gif_duration is not None:
    for clip in gif_clips:
      clip.set_duration(gif_duration)

  combined_clip = mp.concatenate_videoclips(gif_clips, method='compose')

  if outfile is not None:
    combined_clip.write_videofile(outfile, codec='mpeg4')

  return combined_clip

def get_beat_timestamps(audio: Audio):
  """..."""
  tempo, beat_frames = librosa.beat.beat_track(y=audio.waveform, sr=audio.samplerate)
  return librosa.frames_to_time(beat_frames, sr=sr)

def attach_audio_to_video(path_to_audio: Audio, video: mp.VideoFileClip, outfile = None):
  """
  overlays audio on a moviepy video clip
  """
  audio = mp.AudioFileClip(path_to_audio)

  if audio.duration > video.duration:
    audio.set_duration(video.duration)

  video.audio = mp.afx.audio_loop(audio, duration=video.duration)

  if outfile is not None:
    video.write_videofile(outfile, codec='libx264', audio_codec='aac')

  return video

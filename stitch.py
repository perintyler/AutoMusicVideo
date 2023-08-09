"""stitch.py"""

import librosa

import moviepy.editor as mp

def create_video_from_gifs(infiles, outfile = None) -> mp.VideoFileClip:
  gif_clips = map(mp.VideoFileClip, infiles)
  combined_clip = mp.concatenate_videoclips(gif_clips)
  if outfile is not None:
    combined_clip.write_videofile(outfile)
  return combined_clip

def get_beat_timestamps(audio):
  """..."""
  tempo, beat_frames = librosa.beat.beat_track(y=audio.waveform, sr=audio.samplerate)
  return librosa.frames_to_time(beat_frames, sr=sr)


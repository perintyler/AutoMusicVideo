"""AutoMusicVideo::editing_room.audio

This module provides a lightweight `Audio` class that encapsulates a waveform 
and a sample rate and can be loaded from an audio files or downloaded from
the cloud storage with a song id
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
from moviepy.editor import AudioClip, VideoClip, afx as after_effects
import librosa
import numpy

import storyboard

@dataclass
class Audio:
  """lightweight class to encapsulate an audio's waveform and samplerate"""
  
  waveform: numpy.ndarray
  samplerate: int
  path: Path = None

  @property
  def num_channels(self):
    """
    """
    return self.waveform.shape[0] if len(self.waveform.shape) >= 2 else 1

  def is_mono(self) -> bool:
    """
    """
    return self.num_channels == 1

  def is_stereo(self) -> bool:
    """
    """
    return self.num_channels == 2

  @property
  def num_samples(self):
    """
    """
    return len(self.waveform) if self.is_mono() else self.waveform.shape[1]

  @property
  def duration(self) -> float:
    """
    returns the length of the audio clip in seconds
    """
    return self.num_samples / self.samplerate

  def as_mono(self) -> 'Audio':
    """
    """
    return Audio(numpy.mean(self.waveform, axis=0), self.samplerate, self.path)

  def get_channel(self, channel):
    """
    """
    assert channel < self.num_channels
    return self.waveform[:,channel] if not self.is_mono() else self.waveform

  def get_amplitude(self, timestamp, channel) -> float:
    """
    """
    assert channel < self.num_channels
    sample_index = int(timestamp * self.samplerate)
    return self.get_channel(channel)[sample_index]

  def sample(self, timestamp) -> Tuple[float]:
    """
    """
    return tuple(self.get_amplitude(timestamp, channel) for channel in range(self.num_channels))

  def as_clip(self) -> AudioClip:
    """
    returns this audio as a `moviepy` clip
    """
    return AudioClip(lambda t: self.sample(t), duration=self.duration, fps=self.samplerate)

  def attach_to(self, video_clip: VideoClip) -> VideoClip:
    """
    overlays this audio onto the given video clip
    """
    audio_clip = self.as_clip()
    audio_clip.set_duration(video_clip.duration if video_clip.duration >= self.duration else self.duration)
    video_clip.audio = after_effects.audio_loop(audio_clip, duration=video_clip.duration)
    return video_clip

  def save_as_wav(self, outfile: Path, normalize_audio = False):
    """
    writes the waveform to a WAV file
    """
    librosa.output.write_wav(self.waveform, self.samplerate, normalize = normalize_audio)

  @classmethod
  def load(Cls, audio_file: Path):
    """
    reads the wavefrom and sample rate from a locally written audio file
    """
    assert audio_file.exists()
    waveform, samplerate = librosa.load(str(audio_file), mono=False, sr=None)
    return Cls(waveform, samplerate, audio_file)

  @classmethod
  def download(Cls, song_id: str):
    """
    reads the wavefrom and sample rate from an audio file stored in the input audio storage bucket
    """
    audio_bytes = storyboard.cloud_storage.inputs.get_audio_bytes(song_id)
    waveform, samplerate = librosa.load(audio_bytes, mono=False, sr=None)
    return Cls(waveform, samplerate, Path(song_id))

  def __repr__(self):
    filename = f'"{str(self.path.stem)}"' if self.path else None
    return f'<Audio channels={self.num_channels} samples={self.num_samples} samplerate={self.samplerate} filename={filename}>'
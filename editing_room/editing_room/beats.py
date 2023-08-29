"""AutoMusicVideo::editing_room.beats"""

import librosa
from typing import List
from dataclasses import dataclass
from .audio import Audio

@dataclass
class Beats:
  """timestamp pulses in a song"""

  timestamps: List[float]

  def get_closest(self, timestamp):
    """
    returns the time for the beat that's closest to the given timestamp
    """
    num_beats = len(self.timestamps)

    if num_beats == 0:  return None
    elif timestamp < 0: return self.timestamps[0]

    for beat_index in range(num_beats-1):

      early_beat_timestamp = self.timestamps[beat_index]
      late_beat_timestamp = self.timestamps[beat_index+1]

      if timestamp > early_beat_timestamp and timestamp < late_beat_timestamp:
        time_since_early_beat = timestamp - early_beat_timestamp
        time_until_late_beat = late_beat_timestamp - timestamp
        return early_beat_timestamp if time_since_early_beat < time_until_late_beat else late_beat_timestamp
    
    return self.timestamps[-1] # the given timestamp occurs after the last beat, so return the last beat

  @classmethod
  def load(Cls, audio: Audio):
    """
    find pulses in audio using the `librosa` framework
    """
    tempo, beat_frames = librosa.beat.beat_track(y=audio.waveform, sr=audio.samplerate)
    timestamps = librosa.frames_to_time(beat_frames, sr=audio.samplerate)
    return Cls([round(t, 3) for t in timestamps])

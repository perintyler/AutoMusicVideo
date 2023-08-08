"""isolate_vocals.py"""

import librosa
import soundfile as sf
import numpy as np
from audio import Audio

def isolate_vocals(audio, outfile=None):
  assert type(audio) is Audio

  S_full, phase = librosa.magphase(librosa.stft(audio.waveform))

  # We'll compare frames using cosine similarity, and aggregate similar frames
  # by taking their (per-frequency) median value.
  #
  # To avoid being biased by local continuity, we constrain similar frames to be
  # separated by at least 2 seconds.
  #
  # This suppresses sparse/non-repetetitive deviations from the average spectrum,
  # and works well to discard vocal elements.

  S_filter = librosa.decompose.nn_filter(
    S_full,
    aggregate = np.median,
    metric    = 'cosine',
    width     = int(librosa.time_to_frames(2, sr=audio.samplerate))
  )

  # The output of the filter shouldn't be greater than the input
  # if we assume signals are additive.  Taking the pointwise minimium
  # with the input spectrum forces this.
  S_filter = np.minimum(S_full, S_filter)

  # We can also use a margin to reduce bleed between the vocals and instrumentation masks.
  # Note: the margins need not be equal for foreground and background separation
  margin_i, margin_v = 2, 10
  power = 2

  mask_i = librosa.util.softmask(S_filter,
                                 margin_i * (S_full - S_filter),
                                 power=power)

  mask_v = librosa.util.softmask(S_full - S_filter,
                                 margin_v * S_filter,
                                 power=power)

  # Once we have the masks, simply multiply them with the input spectrum
  # to separate the components

  S_foreground = mask_v * S_full
  S_background = mask_i * S_full
  updated_waveform = librosa.istft(S_foreground*phase)

  if outfile is not None:
    sf.write(outfile, updated_waveform, samplerate=audio.samplerate, subtype='PCM_24')

  return Audio(updated_waveform, audio.samplerate)


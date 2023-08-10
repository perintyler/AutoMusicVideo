
import json
from dataclasses import dataclass
from typing import List
import pathlib

from lyrics import Lyrics

@dataclass
class MusicVideoSegment:
  """..."""

  bar: Bar
  path_to_multimedia: pathlib.Path = None

  def is_complete(self):
    """
    """
    return self.path_to_multimedia is not None

  def set_multimedia(self, filepath):
    """
    """
    self.path_to_multimedia = filepath if isinstance(filepath, pathlib.Path) else pathlib.Path(filepath)

  def get_multimedia_type(self):
    """
    returns the extension of the segment's multimedia file
    """
    assert self.is_complete()
    return self.path_to_multimedia.suffix

  def __dict__(self):
    return {
      'bar': self.bar.as_dict(),
      'gif': str(self.path_to_multimedia)
    }

@dataclass
class MusicVideo:
  """..."""

  segments: List[MusicVideoSegment]
  source_file: str

  def is_complete(self):
    """
    ...
    """
    for segment in self.segments:
      if not segment.is_complete():
        return False
    return True

  def generate_incomplete_segments(self):
    """
    yields each incomplete `MusicVideoSegment`
    """
    for segment in self.segments:
      if not segment.is_complete():
        yield segment

  def add_multimedia(self, line_number, filepath):
    """
    sets the multimedia path for given line number's `MusicVideoSegment`

    Note: if the segment is already complete (i.e. already has multimedia), the existing
          multimedia is replaced.
    """
    assert line_number > 0
    segment_index = line_number - 1
    segment = self.segments[segment_index]
    assert segment.line_number == line_number
    segment.set_multimedia(filepath)

  def save_as_json(self, outfile):
    """
    serializes all bars and their corresponding multimedia (if the multimedia exists)
    """
    assert outfile.endswith('.json')

    json_contents = {
      'segments':  [segment.as_dict() for segment in self.segments],
      'source_file': self.source_file
    }

    with open(outfile, 'w') as lyrics_json_file:
      json.dump(json_contents, lyrics_json_file)

    return json_contents

  def compile(self):
    """
    stitches together the multimedia of each `MusicVideoSegment`, overlays the audio,
    and saves the final results to an mp4 file
    """
    assert self.is_complete()
    pass

  @classmethod
  def load_from_json(Cls, filepath):
    """
    ...
    """
    all_segments = []

    with open(filepath, 'r') as json_file:
      json_contents = json.load(json_file)

    for segment_json in json_contents:
      bar = Bar.from_json(segment_json['bar'])
      path_to_gif = pathlib.Path(segment_json['gif'])
      segment = MusicVideoSegment(bar, path_to_gif)
      all_segments.append(segment)

    return Cls(all_segments, json_contents['source_file'])

  @classmethod
  def create_new(Cls, path_to_song):
    lyrics = Lyrics.load_from_audio(path_to_song)
    segments = [MusicVideoSegment(bar) for bar in lyrics.bars]
    return Cls(segments, lyrics.source_file)




"""storyboard.py"""

import os
import json
from dataclasses import dataclass
from typing import List
import pathlib

from lyrics import Lyrics, Bar

@dataclass
class StoryboardChapter:
  """rename to StoryboardChapter"""

  bar: Bar
  multimedia: pathlib.Path = None

  def is_complete(self):
    """a chapter is complete if multimedia has been generated for the corresponding lyric
    """
    return self.multimedia is not None

  def get_multimedia_type(self):
    """returns the file type of the chapter's multimedia
    """
    return self.multimedia.suffix if self.is_complete() else None

  def set_multimedia(self, filepath):
    """set a path to a gif, image, or video to be displayed for this chapter
    """
    self.multimedia = filepath if isinstance(filepath, pathlib.Path) else pathlib.Path(filepath)

  def as_dict(self):
    """serializes all chapter properties
    """
    return {
      'bar': self.bar.as_dict(),
      'multimedia': None if self.multimedia is None else str(self.multimedia)
    }

@dataclass
class Storyboard:
  """rename to storyboard"""

  chapters: List[StoryboardChapter]
  source_file: str

  def is_complete(self):
    """a chapter is complete if it a multimedia file exists for the chapter's lyrics
    """
    for chapter in self.chapters:
      if not chapter.is_complete():
        return False
    return True

  def save_as_json(self, outfile):
    """serializes all bars and their corresponding multimedia (if the multimedia exists)
    """
    assert outfile.endswith('.json')

    json_contents = {
      'chapters':  [chapter.as_dict() for chapter in self.chapters],
      'source_file': self.source_file
    }

    with open(outfile, 'w') as lyrics_json_file:
      json.dump(json_contents, lyrics_json_file, indent=2)

    return json_contents

  @classmethod
  def load_from_json(Cls, filepath):
    """creates and returns an instance of `Storyboard` using a chapters JSON file (see README)
    """
    chapters = []

    assert os.path.exists(filepath)

    with open(filepath, 'r') as json_file:
      json_contents = json.load(json_file)

    for json_chapter in json_contents['chapters']:
      bar = Bar.from_json(json_chapter['bar'])
      path_to_multimedia = None if json_chapter['multimedia'] is None else pathlib.Path(json_chapter['multimedia'])
      chapters.append(StoryboardChapter(bar, path_to_multimedia))

    return Cls(chapters, json_contents['source_file'])

  @classmethod
  def create_new(Cls, path_to_song):
    """...
    """
    lyrics = Lyrics.load_from_audio(path_to_song)
    chapters = [StoryboardChapter(bar) for bar in lyrics.bars]
    return Cls(chapters, lyrics.source_file)




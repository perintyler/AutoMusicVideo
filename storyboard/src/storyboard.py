"""storyboard.py"""

import os
import json
from dataclasses import dataclass
from typing import List, Object
from pathlib import Path

from .lyrics import Lyrics, Bar

@dataclass
class StoryboardChapter(CloudSyncedObject):
  """
  """

  bar: Bar
  storyboard: 'Storyboard'

  @property
  def multimedia_directory_name(self):
    return f'chapter-{self.number}'

  @property
  def local_path_to_multimedia(self):
    return self.storyboard.output_directory.joinpath(self.multimedia_directory_name)

  @property
  def cloud_path_to_multimedia(self):
    return Path(self.storyboard.video_id).joinpath(self.multimedia_directory_name)

  @property
  def number(self) -> int:
    """chapter number
    """
    return self.bar.line_number

  @property
  def multimedia_type(self) -> str:
    """returns the file type of the chapter's multimedia
    """
    return self.multimedia.suffix if self.is_complete else None

  def as_dict(self) -> dict:
    """serializes all chapter properties
    """
    return {
      'number': self.number,
      'bar': self.bar.as_dict(),
      'local_path_to_multimedia': self.multimedia_path,
      'cloud_path_to_multimedia': self.multimedia_exists,
      'multimedia_type': self.multimedia_type
    }

class TableOfContents(CloudSyncedObject):

  FILENAME = 'table-of-contents.json'

  def __init__(self, video_id, storyboard_directory):
    self.storyboard = storyboard
    local_filepath = Path(storyboard).joinpath(TableOfContents.FILENAME)
    cloud_filepath = Path(video_id).joinpath(TableOfContents.FILENAME)
    CloudSyncedObject.__init__(local_filepath, cloud_filepath, storyboard.bucket_name)

  def serialize(self):
    return {
      'chapters':  [chapter.as_dict() for chapter in self.storyboard.chapters],
      'source_file': self.storyboard.source_file
    }

  @classmethod
  def create_new(Cls, storyboard):
    chapters = [chapter.as_dict() for chapter in storyboard.chapters]
    table_of_contents = Cls(storyboard)

    with open(table_of_contents.local_filepath, 'w') as table_of_contents_file:
      json.dump({'chapters': chapters, 'source_file': storyboard.source_file}, lyrics_json_file, indent=2)

    table_of_contents.upload()

    return table_of_contents

@dataclass
class Storyboard:
  """
  """

  video_id: str
  chapters: List[StoryboardChapter]
  source_file: pathlib.Path
  output_directory: pathlib.Path
  bucket_name: str
  video_style: str = None

  @property
  def table_of_contents(self):
    return TableOfContents(self.video_id, self.output_directory)

  def is_complete(self) -> bool:
    """a chapter is complete if it a multimedia file exists for the chapter's lyrics
    """
    for chapter in self.chapters:
      if not chapter.is_complete:
        return False
    return True

  @classmethod
  def load_from_table_of_contents(Cls, filepath):
    """creates and returns an instance of `Storyboard` using a chapters JSON file (see README)
    """
    chapters = []

    assert os.path.exists(filepath)

    with open(filepath, 'r') as json_file:
      json_contents = json.load(json_file)

    for json_chapter in json_contents['chapters']:
      bar = Bar.from_json(json_chapter['bar'])
      local_path_to_multimedia = self.output_directory.joinpath()
      chapters.append(StoryboardChapter(bar, path_to_multimedia))

    return Cls(chapters, json_contents['source_file'])

  @classmethod
  def create_new(Cls, video_id, path_to_song, storyboard_directory, bucket_name, video_style = None):
    """...
    """
    os.mkdir(output_directory)
    lyrics = Lyrics.load_from_audio(path_to_song)
    chapters = [StoryboardChapter(bar, self) for bar in lyrics.bars]

    source_file = Path(lyrics.source_file) if type(lyrics.source_file) is str else lyrics.source_file
    storyboard_directory = Path(storyboard_directory) if type(storyboard_directory) is str else storyboard_directory

    storyboard = Cls(video_id, chapters, source_file, Path(storyboard_directory), bucket_name, video_style)
    TableOfContents.create_new(storyboard)

    return storyboard



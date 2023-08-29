"""storyboard.py"""

import os
import json
from dataclasses import dataclass
from typing import List
from pathlib import Path

from . import cloud_storage
from . import config

from .lyrics import Lyric

BUCKET_NAME = config.get_storyboard_bucket_name()

@dataclass
class StoryboardChapter:
  """
  """

  song_id: str
  style: str
  lyric: Lyric

  @property
  def number(self) -> int:
    """chapter number
    """
    return self.lyric.line_number

  @property
  def multimedia(self) -> Path:
    """path to directory containing multimedia for the chapter
    """
    return Path(self.song_id).joinpath(f'chapter-{self.number}')

  def as_dict(self) -> dict:
    """serializes all chapter properties
    """
    return {
      'lyric': self.lyric.as_dict(),
      'multimedia': str(self.multimedia),
    }

  @classmethod
  def from_json(Cls, song_id, style, json_chapter):
    """
    """
    lyric = Lyric.from_json(json_chapter['lyric'])
    return Cls(song_id, style, lyric)

@dataclass
class TableOfContents:

  FILENAME = 'table-of-contents.json'

  song_id: str
  video_style: str
  bucket_name: str
  chapters: List[StoryboardChapter]

  def serialize(self):
    """
    """
    return {
      'song_id': self.song_id,
      'video_style': self.video_style,
      'path': str(TableOfContents.path(self.song_id)),
      'bucket_name': self.bucket_name,
      'chapters':  [chapter.as_dict() for chapter in self.chapters],
    }

  def upload(self):
    cloud_storage.upload_json(
      self.serialize(), 
      TableOfContents.path(self.song_id), 
      self.bucket_name
    )

  def delete(self):
    cloud_storage.delete_file(
      TableOfContents.path(self.song_id), 
      self.bucket_name
    )

  @classmethod
  def path(Cls, song_id):
    return Path(song_id).joinpath(Cls.FILENAME)

  @classmethod
  def exists(Cls, song_id):
    path = Cls.path(song_id)
    return cloud_storage.file_exists(path, BUCKET_NAME)

  @classmethod
  def from_json(Cls, json_table_of_contents):
    """
    """
    song_id = json_table_of_contents['song_id']
    video_style = json_table_of_contents['video_style']
    bucket_name = json_table_of_contents['bucket_name']
    chapters = [StoryboardChapter.from_json(song_id, video_style, json_chapter) \
                  for json_chapter in json_table_of_contents['chapters']]

    return Cls(song_id, video_style, bucket_name, chapters) 


  @classmethod
  def download(Cls, song_id):
    path = Cls.path(song_id)
    json_table_of_contents = cloud_storage.download_json(path, BUCKET_NAME)
    return Cls.from_json(json_table_of_contents)

  @classmethod
  def create_new(Cls, song_id, audio_file, video_style=None):
    """
    """
    all_lyrics = Lyric.load_all_from_audio(str(audio_file))

    table_of_contents = Cls(
      song_id, 
      video_style,
      BUCKET_NAME,
      [StoryboardChapter(song_id, video_style, lyric) for lyric in all_lyrics], 
    )

    table_of_contents.upload()

    return table_of_contents

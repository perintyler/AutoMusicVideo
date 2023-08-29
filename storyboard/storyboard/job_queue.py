"""job.py"""

import os
import json
from pathlib import Path
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import List

from . import config
from . import cloud_storage
from .storyboard import StoryboardChapter, TableOfContents

BUCKET_NAME = config.get_storyboard_bucket_name()

def generate_prompt(chapter: StoryboardChapter):
  """
  """
  text_input = chapter.lyric.text
  style = chapter.style
  return text_input if style is None else f'{text_input} in the style of {style}'

class JobStatus(Enum):
  """"""
  IDLE        = 'idle'
  IN_PROGRESS = 'in_progress'
  DONE        = 'done'
  FAILED      = 'failed'

  def serialize(self) -> str:
    """returns a string that can be stored in JSON
    """
    return self.value

  @classmethod
  def from_json(Cls, json_status):
    """
    """
    return Cls(json_status)

@dataclass
class StoryboardJob:

  job_id: int
  prompt: str
  style: str
  output_directory: Path
  status: JobStatus

  def is_idle(self): return self.status is JobStatus.IDLE
  def is_done(self): return self.status is JobStatus.DONE
  def in_progress(self): return self.status is JobStatus.IN_PROGRESS

  def set_status(self, updated_status):
    self.status = updated_status

  def serialize(self):
    """
    """
    return {
      "job_id": self.job_id,
      "prompt": self.prompt,
      "style": self.style,
      "output_directory": str(self.output_directory),
      "status": self.status.serialize()
    }

  @classmethod
  def from_json(Cls, props: dict):
    """
    """
    return Cls(
      int(props['job_id']),
      props['prompt'], 
      props['style'],
      Path(props['output_directory']), 
      JobStatus.from_json(props['status'])
    )

  @classmethod
  def create_new(Cls, chapter: StoryboardChapter):
    """
    """
    job_id = chapter.number
    prompt = generate_prompt(chapter)
    style = chapter.style
    output_directory = chapter.multimedia
    status = JobStatus.IDLE
    return Cls(job_id, prompt, style, output_directory, status)

@dataclass
class StoryboardJobQueue:

  FILENAME = 'job-queue.json'

  song_id: str
  bucket_name: str
  jobs: List[StoryboardJob]

  def get_job(self, job_id):
    """
    """
    return next((job for job in self.jobs if job.job_id == job_id), None)

  def get_idle_jobs(self):
    return list(filter(lambda job: job.is_idle(), self.jobs))

  def get_completed_jobs(self):
    return list(filter(lambda job: job.is_done(), self.jobs))

  def get_jobs_in_progress(self):
    return list(filter(lambda job: job.in_progress(), self.jobs))

  def num_jobs(self)             : return len(self.jobs)
  def num_idle_jobs(self)        : return len(self.get_idle_jobs())
  def num_completed_jobs(self)   : return len(self.get_completed_jobs())
  def num_jobs_in_progress(self) : return len(self.get_jobs_in_progress())

  def is_complete(self):
    """returns true if all jobs have been marked as DONE
    """
    return len(self.get_completed_jobs()) == self.num_jobs()

  def has_idle_jobs(self):
    """
    """
    return self.num_idle_jobs() > 0

  def next_job(self) -> StoryboardJob:
    """returns a job that hasn't been started, or None if there are no idle jobs

    The job won't be removed from the queue file until it is marked as complete
    """
    idle_jobs = self.get_idle_jobs()

    if len(idle_jobs) == 0:
      next_job = None
    else:
      next_job = idle_jobs[0]
      next_job.set_status(JobStatus.IN_PROGRESS)

    return next_job

  def finish_job(self, job_id):
    """
    """
    self.get_job(job_id).set_status(JobStatus.DONE)

  def serialize(self):
    """
    """
    return {
      'song_id': self.song_id,
      'path': str(StoryboardJobQueue.path(self.song_id)),
      'bucket_name': self.bucket_name,
      'jobs': [job.serialize() for job in self.jobs]
    }

  def upload(self):
    """
    """
    cloud_storage.upload_json(
      self.serialize(), 
      StoryboardJobQueue.path(self.song_id), 
      self.bucket_name
    )

  def delete(self):
    """
    """
    return cloud_storage.delete_file(
      StoryboardJobQueue.path(self.song_id),
      BUCKET_NAME
    )

  @classmethod
  def path(Cls, song_id):
    return Path(song_id).joinpath(Cls.FILENAME)

  @classmethod
  def exists(Cls, song_id):
    """
    """
    return cloud_storage.file_exists(
      StoryboardJobQueue.path(song_id),
      BUCKET_NAME
    )

  @classmethod
  def create_new(Cls, table_of_contents):
    """
    """
    job_queue = Cls(
      table_of_contents.song_id,
      table_of_contents.bucket_name,
      [StoryboardJob.create_new(chapter) for chapter in table_of_contents.chapters]
    )
    job_queue.upload()
    return job_queue

  @classmethod
  def download(Cls, song_id):
    job_queue_json = cloud_storage.download_json(Cls.path(song_id), BUCKET_NAME)
    return Cls(
      job_queue_json['song_id'],
      job_queue_json['bucket_name'],
      [StoryboardJob.from_json(job_json) for job_json in job_queue_json['jobs']]
    )

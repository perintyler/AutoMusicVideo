"""job.py"""

import os
import json
from pathlib import Path
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from .cloud_sync import CloudSyncedObject

def generate_prompt(chapter):
  """TODO
  """
  text_input = chapter.bar.text
  style = chapter.storyboard.video_style
  if style is None:
    return text_input
  else:
    return f'{text_input} in the style of {style}'

def serialize_job_queue(video_id, bucket_name, jobs):
  """
  """
  return {
    'video_id': video_id,
    'bucket': bucket,
    'jobs': [job.serialize() for job in jobs]
  }

class JobStatus(Enum):
  """"""
  IDLE        = 'idle'
  IN_PROGRESS = 'in_progress'
  DONE        = 'done'
  FAILED      = 'failed'

  def serialize(self) -> str:
    """returns a string that can be stored in JSON"""
    return self.value

@dataclass
class TextToImageJob:

  job_id: int
  prompt: str
  local_output_directory: Path
  cloud_output_directory: Path
  status: JobStatus

  def serialize(self):
    """
    """
    return {
      "prompt": self.prompt,
      "local_output_directory": self.local_output_directory,
      "cloud_output_directory": self.cloud_output_directory,
      "status": self.status.serialize()
    }

  @classmethod
  def from_json(Cls, props: dict):
    """
    """
    return Cls(
      int(props['id']),
      str(props['prompt']), 
      Path(props['local_output_directory']), 
      Path(props['cloud_output_directory']),
      JobStatus(props['status'])
    )

  @classmethod
  def create_new(Cls, chapter: StoryboardChapter):
    """
    """
    job_id = chapter.number
    prompt = generate_prompt(chapter)
    local_output_directory = chapter.local_path_to_multimedia
    cloud_output_directory = chapter.cloud_path_to_multimedia
    status = JobStatus.IDLE
    return Cls(job_id, prompt, local_path_to_multimedia, cloud_path_to_multimedia, status)

@dataclass
class StoryboardJobQueue(CloudSyncedObject):

  FILENAME = 'job-queue.json'

  def __init__(self, storyboard, bucket_name):
    """this constructor shouldn't be called directly. instead, use `StoryboardJobQueue.get`
    """
    self.storyboard = storyboard
    CloudSyncedObject.__init__(
      storyboard.local_directory.joinpath(StoryboardJobQueue.FILENAME), 
      storyboard.cloud_directory.joinpath(StoryboardJobQueue.FILENAME), 
      bucket_name
    )

  @property
  def jobs(self):
    """
    """
    return [TextToImageJob.from_json(job_json) for job_json in self.read().get('jobs', [])]

  def serialize(self):
    """
    """
    return {
      'video_id': self.storyboard.video_id,
      'bucket': self.bucket,
      'jobs': [job.serialize() for job in self.jobs]
    }

  def pop(self) -> TextToImageJob:
    """returns a job that hasn't been started, or None if there are no idle jobs

    The job won't be removed from the queue file until it is marked as complete
    """
    for job in self.jobs:
      if not job.in_progress:
        job.in_progress = True
        self.sync()
        return job

    return None

  def delete_job(self, output_directory):
    """
    """
    with open(self.filepath) as queue_file:
      job_queue = json.load(queue_file)['jobs']

    for job_index, job in enumerate(self._iterate_jobs()):
      if job.output_directory == output_directory:
        job_queue.pop(job_index)
        break

  def has_job(self, output_directory):
    """
    """
    for job in self._iterate_jobs():
      if job.output_directory == output_directory:
        return True

    return False

  def is_complete(self):
    """returns true if there are no idle jobs
    """
    for job in self.jobs:
      if job.status is not JobStatus.DONE:
        return False
    return True

  def has_idle_jobs(self):
    """
    """
    for job in self.jobs:
      if job.status is JobStatus.IDLE:
        return True
    return False

  def num_jobs_in_progress(self):
    """
    """
    return len(filter(lambda job: job.status is JobStatus.IN_PROGRESS, self.jobs))

  @classmethod
  def get(Cls, storyboard):
    """
    """
    job_queue = Cls(storyboard)

    if not job_queue.local_filepath.exists():

      bucket_name = get_storyboard_bucket_name()
      jobs = [Job.create_new(chapter) for chapter in storyboard.chapters]
      serialized_queue = serialize_job_queue(storyboard.video_id, bucket_name, jobs)

      with open(job_queue.local_filepath, 'w') as job_queue_file:
        json.dump(serialized_queue, job_queue_file, indent=2)

      job_queue.upload()

    return job_queue

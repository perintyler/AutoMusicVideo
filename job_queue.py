"""job.py"""

import os
import json
import pathlib
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

class CloudService(Enum):
  """supported services for text-to-image in the cloud"""

  GOOGLE_COMPUTE_ENGINE = "GCP"
  GOOGLE_COLLAB = "Collab"
  KAGGLE = "Kaggle"
  AWS_EC2 = "EC2"

@dataclass
class TextToImageJob:

  prompt: str
  output_directory: pathlib.Path
  in_progress: bool # TODO: change this to start_time (None if not in progress) so hanging jobs can be dealt with

  def as_dict(self):
    return {
      "prompt": self.prompt,
      "output_directory": self.output_directory,
      "in_progress": self.in_progress
    }

  @classmethod
  def from_dict(Cls, props: dict):
    return Cls(props['prompt'], props['output_directory'], props['in_progress'])

@dataclass
class TextToImageJobQueue:

  def __init__(self, filepath):
    self.filepath = filepath

    if not os.path.exists(filepath):
      with open(filepath, 'w') as queue_file:
        json.dump({
          'timestamp': datetime.now().strftime("%m-%d-%y_%H-%M-%S"),
          'jobs': []
        }, queue_file, indent=2)

  def _iterate_jobs(self):
    """reads the queue file to create and yield instances of `TextToImageJob`
    """
    with open(self.filepath) as queue_file:
      job_queue = json.load(queue_file)['jobs']

    for job_dict in job_queue:
      yield TextToImageJob.from_dict(job_dict)

  def get_next_job(self):
    """returns a job that hasn't been started, or None if there are no idle jobs

    The job won't be removed from the queue file until it is marked as complete
    """    
    for job in self._iterate_jobs():
      if not job.in_progress():
        return job

    return None

  def add_job(self, prompt, output_directory):
    """
    """
    with open(self.filepath) as queue_file:
      queue_file_contents = json.load(queue_file)

    queue_file_contents['jobs'].append({
      'prompt': prompt, 
      'output_directory': output_directory, 
      'in_progress': False
    })

    with open(self.filepath, 'w') as queue_file:
      json.dump(queue_file_contents, queue_file, indent=2)

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

  def is_empty(self):
    """returns true if there are no idle jobs
    """
    return self.get_next_job() is None

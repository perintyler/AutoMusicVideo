
import json
from importlib.resources import files

from .storyboard import TableOfContents
from .job_queue import StoryboardJobQueue, JobStatus

with open(files('storyboard.data').joinpath('test-table-of-contents.json')) as table_of_contents_file:
  table_of_contents = TableOfContents.from_json(json.load(table_of_contents_file))
  job_queue = StoryboardJobQueue.create_new(table_of_contents)

def test_job_queue_exists():
  assert job_queue is not None
  assert StoryboardJobQueue.exists(job_queue.song_id)

def test_jobs_new_jobs_are_idle():
  for job in job_queue.jobs:
    assert job.is_idle()
    assert job.status is JobStatus.IDLE

def test_download_job_queue():
  assert StoryboardJobQueue.download(job_queue.song_id).serialize() == job_queue.serialize()

def test_jobs_have_prompts():
  for job in job_queue.jobs:
    assert job.prompt is not None
    assert type(job.prompt) is str
    assert len(job.prompt) > 0

def test_jobs_have_output_directories():
  for job in job_queue.jobs:
    assert job.output_directory is not None

def test_pop_and_finish_job():
  first_job = job_queue.jobs[0]
  assert first_job.is_idle()
  assert job_queue.num_jobs_in_progress() == 0

  next_job = job_queue.next_job()
  assert next_job.job_id == first_job.job_id
  assert not next_job.is_idle()
  assert next_job.in_progress()
  assert job_queue.num_jobs_in_progress() == 1

  job_queue.finish_job(next_job.job_id)
  assert next_job.is_done()
  assert job_queue.num_jobs_in_progress() == 0
  assert job_queue.num_completed_jobs() == 1

def test_upload_job_queue():
  job_queue.upload()
  downloaded_job_queue = StoryboardJobQueue.download(job_queue.song_id)
  assert downloaded_job_queue.num_completed_jobs() == 1
  assert job_queue.serialize() == downloaded_job_queue.serialize()

def test_delete_job_queue():
  assert StoryboardJobQueue.exists(job_queue.song_id)
  job_queue.delete()
  assert not StoryboardJobQueue.exists(job_queue.song_id)

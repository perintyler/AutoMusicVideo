"""AutoMusicVideo | go.py"""

import modal
import os
import sys
import pathlib
import subprocess
import asyncio
import time
import cloud_function

@cloud_function.use_gpu
async def do_next_job(song_id):
  """
  """
  import storyboard
  job = next(storyboard.generate_jobs())
  if job:
    print(f'doing job for {song_id}: {job.as_dict()}')
    storyboard.do_job(song_id, job)
  else:
    print('no jobs left')

@cloud_function.use_cpu
async def make_storybooks():
  """
  """
  import storyboard

  input_audio_directory = pathlib.Path('/AutoMusicVideo').joinpath('input-audio')

  for song_path in input_audio_directory.iterdir():
    song_id = song_path.stem
    print(f'writing table of contents for {song_id}')
    storyboard.write_table_of_contents(song_id, song_path)
    for job in storyboard.generate_jobs(song_id):
      storyboard.do_job(song_id, job)

    # await asyncio.gather(
    #   *[do_storyboard_job.remote.aio(song_id, job) for job in storyboard.generate_jobs(song_id)]
    # )

@cloud_function.entrypoint
def main():
  """
  """
  make_storybooks.remote()

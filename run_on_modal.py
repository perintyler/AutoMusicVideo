
import os
import sys
import pathlib
import subprocess
import modal
import asyncio
import time

INPUT_AUDIO_DIRECTORY = os.path.join('/AutoMusicVideo', 'input-audio')

exclude = lambda filepath: not filepath.endswith('__pycache__') and not filepath.endswith('.pyc')

file_mount = modal.Mount \
            .from_local_dir('storyboard', condition=exclude) \
            .add_local_dir('input-audio') \

container_image = modal.Image.from_dockerfile('Dockerfile', context_mount=file_mount)

stub = modal.Stub("storyboard-creation")

@stub.function(
  gpu="A100", 
  image=container_image, 
  secret=modal.Secret.from_name("gcp-storage-secrets"),
  timeout=60*60*24)
async def do_next_job(song_id):
  import storyboard
  job = next(storyboard.generate_jobs())
  if job:
    print(f'doing job for {song_id}: {job.as_dict()}')
    storyboard.do_job(song_id, job)
  else:
    print('no jobs left')

@stub.function(
  gpu="A100", 
  image=container_image, 
  secret=modal.Secret.from_name("gcp-storage-secrets"),
  timeout=60*60*24)
async def make_storybooks():
  import storyboard

  for audio_file in os.listdir(INPUT_AUDIO_DIRECTORY):
    song_path = pathlib.Path(INPUT_AUDIO_DIRECTORY).joinpath(audio_file)
    song_id = song_path.stem
    print(f'making storyboard for {song_id}: {song_path}')
    storyboard.write_table_of_contents(song_id, song_path)
    for job in storyboard.generate_jobs(song_id):
      storyboard.do_job(song_id, job)
    # await asyncio.gather(
    #   *[do_storyboard_job.remote.aio(song_id, job) for job in storyboard.generate_jobs(song_id)]
    # )

@stub.local_entrypoint()
def main():
    make_storybooks.remote()
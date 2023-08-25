
import os
import sys
import subprocess
import modal

exclude = lambda filepath: not filepath.endswith('__pycache__') and not filepath.endswith('.pyc')

file_mount = modal.Mount \
            .from_local_dir('storyboard', condition=exclude) \
            .add_local_dir('input-audio') \
            .add_local_file('config.json')

container_image = modal.Image.from_dockerfile('Dockerfile', context_mount=file_mount)

stub = modal.Stub("storyboard-creation")

@stub.function(image=container_image, secret=modal.Secret.from_name("gcp-storage-secrets"))
def create_storyboard(input_audio, output_directory):
  import storyboard
  print("This code is running on a remote worker!")
  storyboard.main(input_audio, output_directory)

@stub.local_entrypoint()
def main():
  print("Modal Entry Point")
  create_storyboard.call('input-audio/something.mp3', 'something-music-video')

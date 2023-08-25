
import os
import sys
import subprocess
import modal

file_mount = modal.Mount.from_local_dir('storyboard', condition=lambda filepath: not filepath.endswith('__pycache__'))

container_image = modal.Image.from_dockerfile('Dockerfile', context_mount=file_mount)

stub = modal.Stub("storyboard-creation")

@stub.function(image=container_image, secret=modal.Secret.from_name("gcp-storage-secrets"))
def create_storyboard(input_audio, output_directory):
  import storyboard
  print("This code is running on a remote worker!")
  storyboard.create_storyboard(input_audio, output_directory)

@stub.local_entrypoint()
def main():
  print("Modal Entry Point")
  create_storyboard.call('input-audio/something.mp3', 'storyboards/something-music-video')

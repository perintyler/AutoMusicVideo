"""modal_worker.py"""

import modal

file_filter = lambda filepath: not filepath.endswith('__pycache__') \
                           and not filepath.endswith('.pyc')

file_mount = modal.Mount \
            .from_local_dir('storyboard', condition=file_filter) \
            .add_local_dir('input-audio') \
            .add_local_file('config.json')

stub = modal.Stub("storyboard-creation")

@stub.function(
  image  = modal.Image.from_dockerfile('Dockerfile', context_mount=file_mount), 
  gpu    = "A100",
  secret = modal.Secret.from_name("gcp-storage-secrets"))
def create_storyboard(config):
  """modal worker
  """
  import storyboard
  print(f"calling `storyboard.main('{config.input_audio}', '{config.output_directory}')` on a remote worker")
  storyboard.main(input_audio, output_directory)

@stub.local_entrypoint()
def main():
  """local entry point that spawns Modal workers
  """
  create_storyboard.call('config.json')


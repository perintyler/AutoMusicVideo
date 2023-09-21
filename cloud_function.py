"""AutoMusicVideo | cloud_function.py"""

import modal

DEFAULT_NUM_GPUS = 2

T4 = modal.gpu.T4

A100 = modal.gpu.A100

GPU = modal.gpu.T4

DOCKERFILE_PATH = 'Dockerfile'

MODAL_PROJECT_NAME = 'storyboard-creation' # todo: make this an env variable

MODAL_SECRETS_ID = 'gcp-storage-secrets' # todo: make this an env variable

MAX_TIMEOUT = 60*60*24

def entrypoint(f):
  """
  """
  return modal.Stub(MODAL_PROJECT_NAME).local_entrypoint(f)

def cloud_function(gpu=None, timeout=None):
  """
  """
  local_entry_point = modal.Stub(MODAL_PROJECT_NAME).local_entrypoint(local_entrypoint)

  file_filter = lambda filepath: not filepath.endswith('__pycache__') and not filepath.endswith('.pyc')

  file_mount = modal.Mount.from_local_dir('storyboard', condition=file_filter) \
                          .add_local_dir('input-audio')

  return modal.Stub(MODAL_PROJECT_NAME).function(
    gpu     = gpu,
    image   = modal.Image.from_dockerfile(DOCKERFILE_PATH, context_mount=file_mount), 
    secret  = modal.Secret.from_name(MODAL_SECRETS_ID),
    timeout = timeout
  )

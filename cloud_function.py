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

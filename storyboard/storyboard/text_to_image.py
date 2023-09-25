"""imagegen.py"""

import os

from .lyrics import Lyric

from . import config

from .deepdaze import Imagine

MODEL_NAME = 'ViT-B/32' # 'ViT-L/14'

TIMESTAMP_GENERATED_FILES = False

DEFAULT_SAVE_EVERY = 64

DEFAULT_NUM_EPOCHS = 20

DEFAULT_NUM_LAYERS = 24

DEFAULT_NUM_ITERATIONS = 300

def text_to_image(prompt, output_directory, 
  bucket_name = None, 
  num_epochs = None, 
  num_layers = None, 
  num_iterations = None,
  save_every = None
):
  """
  """
  imagine = Imagine(
    text = prompt,

    model_name = MODEL_NAME,
    num_layers = DEFAULT_NUM_LAYERS if num_layers is None else num_layers,
    epochs = DEFAULT_NUM_EPOCHS if num_epochs is None else num_epochs,
    iterations = DEFAULT_NUM_ITERATIONS if num_iterations is None else num_iterations,
    save_every = DEFAULT_SAVE_EVERY if save_every is None else save_every,
    save_progress = True,
    open_folder = False,
    save_date_time = TIMESTAMP_GENERATED_FILES,
    bucket_name = config.get_storyboard_bucket_name() if bucket_name is None else bucket_name,
    output_folder = str(output_directory),
  )

  imagine()

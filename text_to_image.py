"""imagegen.py"""

import os
from deep_daze import Imagine
from lyrics import Bar

MODEL_NAME = 'ViT-B/32' # 'ViT-L/14'

def text_to_image(text_input, output_directory):
  """
  ...
  """

  imagine = Imagine(
      model_name = MODEL_NAME,
      text = text_input,
      num_layers = 24,
      save_every = 64,
      save_progress = True,
      save_date_time = True,
      save_gif=True,
      output_folder=output_directory,
      open_folder=False
  )

  imagine()

if __name__ == '__main__':
  text_to_image('road to nowhere')

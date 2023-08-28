"""imagegen.py"""

import os
from .lyrics import Bar

from .deepdaze import Imagine

MODEL_NAME = 'ViT-B/32' # 'ViT-L/14'

TIMESTAMP_GENERATED_FILES = False

SAVE_EVERY = 1

def generate_prompt(chapter):
  """TODO
  """
  text_input = chapter.bar.text
  style = chapter.storyboard.video_style
  if style is None:
    return text_input
  else:
    return f'{text_input} in the style of {style}'

def text_to_image(job, style = None):
  """
  ...
  """  
  imagine = Imagine(
      model_name = MODEL_NAME,
      text = generate_prompt(chapter),
      num_layers = 24,
      save_every = SAVE_EVERY,
      save_progress = True,
      save_date_time = TIMESTAMP_GENERATED_FILES,
      save_gif=True,
      output_folder=output_directory,
      open_folder=False
  )

  imagine()

if __name__ == '__main__':
  text_to_image('road to nowhere', 'temp-images')

"""imagegen.py"""

import os
from deep_daze import Imagine
from lyrics import Bar

MODEL_NAME = 'ViT-B/32' # 'ViT-L/14'

def generate_image(text):
  """
  ...
  """
  imagined_image_id = '_'.join(text.split(' '))
  imagined_image_directory = os.path.join('images', imagined_image_id)

  if not os.path.exists(imagined_image_directory):
    os.mkdir(imagined_image_directory)

  imagined_image_file = f'{imagined_image_id}-FINAL.jpg'
  path_to_imagined_image = os.path.join(imagined_image_directory, imagined_image_file)

  imagine = Imagine(
      model_name = MODEL_NAME,
      text = text,
      num_layers = 24,
      save_every = 64,
      save_progress = True,
      save_date_time = True,
      save_gif=True,
      output_folder=imagined_image_directory,
      open_folder=False
  )

  imagine()

if __name__ == '__main__':
  generate_image('road to nowhere')

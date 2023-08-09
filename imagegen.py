"""imagegen.py"""

from deep_daze import Imagine

def generate_image(text):
  imagine = Imagine(
      text = text,
      num_layers = 24,
      save_every = 4,
      save_progress = True,
      save_date_time = True,
      save_gif=True
  )

  imagine()

if __name__ == '__main__':
  generate_image('road to nowhere')


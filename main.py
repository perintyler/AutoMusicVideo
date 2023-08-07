"""main.py"""

import os
import time
import json
import numpy as np
import matplotlib.pyplot as plt
import torch

from dalle2_pytorch import (
  DALLE2, 
  DiffusionPriorNetwork, 
  DiffusionPrior, 
  Unet, 
  Decoder, 
  OpenAIClipAdapter
)

TEXT_INPUT = 'road to nowhere'

MODEL_EXISTS = False

NET1_STATE_FILEPATH = "./models/nn1.pth"

NET2_STATE_FILEPATH = "./models/nn2.pth"

NUM_TRAINING_ITERATIONS = 20

VERBOSE = True

LOGFILE_NAME = f'./logs/{time.time()}.json'

# ----------------------------------------------------------------
# ----------------------------------------------------------------

logs = []

images = torch.randn(4, 3, 256, 256)
text = torch.randint(0, 49408, (4, 256))

# openai pretrained clip - defaults to ViT-B/32
clip = OpenAIClipAdapter()

# prior networks (with transformer)

prior_network = DiffusionPriorNetwork(
  dim = 512,
  depth = 6,
  dim_head = 64,
  heads = 8
)

diffusion_prior = DiffusionPrior(
  net = prior_network,
  clip = clip,
  timesteps = 100,
  cond_drop_prob = 0.2
)

unet1 = Unet(
  dim = 128,
  image_embed_dim = 512,
  cond_dim = 128,
  channels = 3,
  dim_mults=(1, 2, 4, 8),
  text_embed_dim = 512,
  cond_on_text_encodings = True  # set to True for any unets that need to be conditioned on text encodings (ex. first unet in cascade)
)

unet2 = Unet(
  dim = 16,
  image_embed_dim = 512,
  cond_dim = 128,
  channels = 3,
  dim_mults = (1, 2, 4, 8, 16)
)

if MODEL_EXISTS:
  print(f'loading unet state from {NET1_STATE_FILEPATH}')
  checkpoint1 = torch.load(NET1_STATE_FILEPATH)
  unet1.load_state_dict(checkpoint1)
  print(f'loading unet state from {NET2_STATE_FILEPATH}')
  checkpoint2 = torch.load(NET2_STATE_FILEPATH)
  unet2.load_state_dict(checkpoint2)

decoder = Decoder(
  unet = (unet1, unet2),
  image_sizes = (128, 256),
  clip = clip,
  timesteps = 1000,
  sample_timesteps = (250, 27),
  image_cond_drop_prob = 0.1,
  text_cond_drop_prob = 0.5
)

# ----------------------------------------------------------------
# ----------------------------------------------------------------

def log(msg):
  """prints if verbose mode is on, otherwise gets written to log file"""
  logs.append(message)
  if (VERBOSE):
    print(f'\t - {msg}')

def print_divider():
  print('')
  print('-'*32)
  print('[]'*16)
  print('-'*32)
  print('')

def train():
  """"""
  def train_diffision_model():
    print('<> training diffusion model <>')
    startTime = time.time()
    for i in range(NUM_TRAINING_ITERATIONS):
      loss = diffusion_prior(text, images)
      loss.backward()
      log(f'loss after iteration #{i+1}: {loss}')
    log(f'DONE -- trained diffusion model in {time.time() - startTime} seconds')

  def train_unets():
    print('<> training unets <>')
    startTime = time.time()
    for i in range(NUM_TRAINING_ITERATIONS):
      for unet_number in (1, 2):
        loss = decoder(images, text = text, unet_number = unet_number) # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
        loss.backward()
        log(f'Loss after iteration {i+1} for #{unet_number} = {loss}')
    log(f'DONE -- trained unets in {time.time() - startTime} seconds')

  train_diffision_model()
  train_unets()

def save_state_to_json():
  """"""
  print('<> saving unet states to JSON files <>')
  for i in (0,1):
    model = decoder.unets[i]
    state = {paramTensor: model.state_dict()[paramTensor].size() for paramTensor in model.state_dict()}
    with open(f'nn{i+1}.json', 'w') as nnStateJSONFile: 
      json.dump(state, nnStateJSONFile)

def save_models():
  """"""
  print('<> saving unet models to PTH files <>')
  log(f'saving models to {NET1_STATE_FILEPATH} and {NET2_STATE_FILEPATH}')
  torch.save(unet1.state_dict(), NET1_STATE_FILEPATH)
  torch.save(unet2.state_dict(), NET2_STATE_FILEPATH)

def save_logs():
  print(f'<> saving logs to {LOGFILE_NAME} <>')
  with open(LOGFILE_NAME, 'w') as logfile:
    json.dump(logs, logfile)

def generate_images(saveToFile=True):
  """"""
  print_divider()
  print(f'<> generating images for input: "{TEXT_INPUT}" <>')
  dalle2 = DALLE2(
    prior = diffusion_prior,
    decoder = decoder
  )

  images = dalle2(
    [TEXT_INPUT],
    cond_scale = 2., # classifier free guidance strength (> 1 would strengthen the condition)
    return_pil_images = True
  )

  log(f'successfully generated {len(images)} images')

  print(f'<> saving images to PNG files <>')
  if saveToFile: # save your image (in this example, of size 256x256)
    numImages = len(list(filter(lambda fn: fn.endswith('.png'), os.listdir('images'))))
    for image, i in enumerate(images):
      imageNumber = numImages + i + 1
      imageFileName = f"images/dalle2-output-{imageNumber}.png"
      plt.imsave(imageFileName, image) # finally save your prediction .
      log(f'saved image #{imageNumber} to {imageFileName}')

  return images

if __name__ == '__main__':
  train()
  save_models()
  generate_images()
  save_logs()



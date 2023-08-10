"""main.py"""

import os
import time
import json
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import torch

import log

from dalle2_pytorch import (
  DALLE2, 
  DiffusionPriorNetwork, 
  DiffusionPrior, 
  Unet, 
  Decoder, 
  OpenAIClipAdapter
)

# --------------------------------------------------------------------------------------------------------------------------------
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# --------------------------------------------------------------------------------------------------------------------------------

TEXT_INPUT = 'road'

USE_PRETRAINED_MODEL = False

NUM_TRAINING_ITERATIONS = 50

START_TIME = datetime.now()

NET1_STATE_FILEPATH = f"./models/UNET1-{START_TIME.isoformat()}.pth"

NET2_STATE_FILEPATH = f"./models/UNET2-{START_TIME.isoformat()}.pth"

# --------------------------------------------------------------------------------------------------------------------------------
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# --------------------------------------------------------------------------------------------------------------------------------

log.header('configuring model')

log.message('loading OpenAI clip adapter')

clip = OpenAIClipAdapter() # openai pretrained clip - defaults to ViT-B/32

log.message('creating the diffusion prior network')

prior_network = DiffusionPriorNetwork(
  dim = 512,
  depth = 6,
  dim_head = 64,
  heads = 8
)

log.message('creating the diffusion prior model')

diffusion_prior = DiffusionPrior(
  net = prior_network,
  clip = clip,
  timesteps = 100,
  cond_drop_prob = 0.2
)

log.message('creating unet #1')

unet1 = Unet(
  dim = 128,
  image_embed_dim = 512,
  cond_dim = 128,
  channels = 3,
  dim_mults=(1, 2, 4, 8),
  text_embed_dim = 512,
  cond_on_text_encodings = True  # set to True for any unets that need to be conditioned on text encodings (ex. first unet in cascade)
)

log.message('creating unet #2')

unet2 = Unet(
  dim = 16,
  image_embed_dim = 512,
  cond_dim = 128,
  channels = 3,
  dim_mults = (1, 2, 4, 8, 16)
)

if USE_PRETRAINED_MODEL:
  log.message(f'loading unet state from {NET1_STATE_FILEPATH}')
  checkpoint1 = torch.load(NET1_STATE_FILEPATH)
  unet1.load_state_dict(checkpoint1)
  log.message(f'loading unet state from {NET2_STATE_FILEPATH}')
  checkpoint2 = torch.load(NET2_STATE_FILEPATH)
  unet2.load_state_dict(checkpoint2)

log.message('creating the decoder')

decoder = Decoder(
  unet = (unet1, unet2),
  image_sizes = (128, 256),
  clip = clip,
  timesteps = 1000,
  sample_timesteps = (250, 27),
  image_cond_drop_prob = 0.1,
  text_cond_drop_prob = 0.5
)

# --------------------------------------------------------------------------------------------------------------------------------
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# --------------------------------------------------------------------------------------------------------------------------------

def save_state_to_json():
  """"""
  log.header('saving unet states to JSON files')
  for i in (0,1):
    model = decoder.unets[i]
    state = {paramTensor: model.state_dict()[paramTensor].size() for paramTensor in model.state_dict()}
    with open(f'nn{i+1}.json', 'w') as nnStateJSONFile: 
      json.dump(state, nnStateJSONFile)

def save_models():
  """"""
  log.header('saving unet models to PTH files')
  log.message(f'saving models to {NET1_STATE_FILEPATH} and {NET2_STATE_FILEPATH}')
  if not os.path.isdir('models'): os.mkdir('models')
  torch.save(unet1.state_dict(), NET1_STATE_FILEPATH)
  torch.save(unet2.state_dict(), NET2_STATE_FILEPATH)

def save_images(images):
  log.header(f'saving images to PNG files')

  if not os.path.isdir('images'): 
    os.mkdir('images')

  numImages = len(list(filter(lambda fn: fn.endswith('.png'), os.listdir('images'))))
  for i, image in enumerate(images):
    imageNumber = numImages + i + 1
    imageFileName = f"images/dalle2-output-{imageNumber}-{START_TIME.isoformat()}.png"
    plt.imsave(imageFileName, image) # finally save your prediction .
    log.message(f'saved image #{imageNumber} to {imageFileName}')

# --------------------------------------------------------------------------------------------------------------------------------
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# --------------------------------------------------------------------------------------------------------------------------------

def train():
  """"""
  # dummy data
  images = torch.randn(4, 3, 256, 256)
  text = torch.randint(0, 49408, (4, 256))

  def train_diffision_model():
    log.header('training diffusion model')
    startTime = time.time()
    for i in range(NUM_TRAINING_ITERATIONS):
      loss = diffusion_prior(text, images)
      loss.backward()
      log.message(f'[loss after iteration #{i+1}]: {loss}')
    log.message(f'DONE: trained diffusion model in {time.time() - startTime} seconds')

  def train_unets():
    
    for unet_number in (1, 2):
      log.header(f'training NN #{unet_number}')
      startTime = time.time()
      for iteration in range(NUM_TRAINING_ITERATIONS):
        loss = decoder(images, text = text, unet_number = unet_number) # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
        loss.backward()
        log.message(f'[loss after iteration {iteration+1}]: {loss}')
      log.message(f'DONE: trained neural net #{unet_number} in {time.time() - startTime} seconds')

  train_diffision_model()
  train_unets()
  log.divider()

def generate_images():
  """"""
  log.header(f'generating images for input: "{TEXT_INPUT}"')
  dalle2 = DALLE2(
    prior = diffusion_prior,
    decoder = decoder
  )

  images = dalle2(
    [TEXT_INPUT],
    cond_scale = 2., # classifier free guidance strength (> 1 would strengthen the condition)
    return_pil_images = True
  )

  log.message(f'successfully generated {len(images)} images')
  log.divider()

  return images

# --------------------------------------------------------------------------------------------------------------------------------
# <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# --------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__': 
  train()
  save_models()
  images = generate_images()
  save_images(images)
  log.save_all()
  log.message(f'finished in {(START_TIME - datetime.now()).seconds} seconds')


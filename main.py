
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

# ----------------------------------------------------------------
# ----------------------------------------------------------------

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

def train():
  """"""
  def train_diffision_model():
    print('training diffusion model')
    loss = diffusion_prior(text, images)
    loss.backward()

  def train_unets():
    print('training unets')
    for unet_number in (1, 2):
      loss = decoder(images, text = text, unet_number = unet_number) # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
      loss.backward()

  train_diffision_model()
  train_unets()

def save_state_to_json():
  """"""
  for i in (0,1):
    model = decoder.unets[i]
    state = {paramTensor: model.state_dict()[paramTensor].size() for paramTensor in model.state_dict()}
    with open(f'nn{i+1}.json', 'w') as nnStateJSONFile: 
      json.dump(state, nnStateJSONFile)

def save_models():
  """"""
  print(f'saving models to {NET1_STATE_FILEPATH} and {NET2_STATE_FILEPATH}')
  torch.save(unet1.state_dict(), NET1_STATE_FILEPATH)
  torch.save(unet2.state_dict(), NET2_STATE_FILEPATH)

def generate_images(saveToFile=True):
  """"""
  print(f'generating images for input: {TEXT_INPUT}')
  dalle2 = DALLE2(
    prior = diffusion_prior,
    decoder = decoder
  )

  images = dalle2(
    [TEXT_INPUT],
    cond_scale = 2., # classifier free guidance strength (> 1 would strengthen the condition)
    return_pil_images = True
  )

  if saveToFile: # save your image (in this example, of size 256x256)
    plt.imsave("images/dalle2_output.png", images[0]) # finally save your prediction .

  return images

if __name__ == '__main__':
  train()
  save_models()
  generate_images()



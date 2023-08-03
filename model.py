# --- model.py --- #

import torch
from dalle2_pytorch import DALLE2, DiffusionPriorNetwork, DiffusionPrior, Unet, Decoder, OpenAIClipAdapter

def get_decoder(stateFile1 = None, stateFile2 = None):
  # openai pretrained clip - defaults to ViT-B/32
  clip = OpenAIClipAdapter()

  # mock data
  text = torch.randint(0, 49408, (4, 256))
  images = torch.randn(4, 3, 256, 256)

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

  loss = diffusion_prior(text, images)
  loss.backward()
  
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

  if stateFile1 is not None:
    checkpoint1 = torch.load(stateFile1)
    unet1.load_state_dict(checkpoint1['model_state_dict'])

  if stateFile2 is not None:
    checkpoint2 = torch.load(stateFile2)
    unet2.load_state_dict(checkpoint2['model_state_dict'])

  return Decoder(
    unet = (unet1, unet2),
    image_sizes = (128, 256),
    clip = clip,
    timesteps = 1000,
    sample_timesteps = (250, 27),
    image_cond_drop_prob = 0.1,
    text_cond_drop_prob = 0.5
  )


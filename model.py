# --- model.py --- #

import torch
from dalle2_pytorch import DALLE2, DiffusionPriorNetwork, DiffusionPrior, Unet, Decoder, OpenAIClipAdapter
import matplotlib.pyplot as plt
import numpy as np

TEXT_INPUT = 'a road to nowhere'

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

# do above for many steps ...

# decoder (with unet)

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

decoder = Decoder(
    unet = (unet1, unet2),
    image_sizes = (128, 256),
    clip = clip,
    timesteps = 1000,
    sample_timesteps = (250, 27),
    image_cond_drop_prob = 0.1,
    text_cond_drop_prob = 0.5
)

def train_model():
    for unet_number in (1, 2):
        loss = decoder(images, text = text, unet_number = unet_number) # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
        loss.backward()

# do above for many steps
def generate_images():
    dalle2 = DALLE2(
        prior = diffusion_prior,
        decoder = decoder
    )

    images = dalle2(
        [TEXT_INPUT],
        cond_scale = 2. # classifier free guidance strength (> 1 would strengthen the condition)
    ).detach().cpu().numpy()

    # save your image (in this example, of size 256x256)

    images = images.squeeze(axis = 0) # since the output is 4D and 0 axis is your batch size of 1 we can squeeze the axis .
    images = np.transpose(images, (1,2,0)) # shifting the channel to last axis as pytorch takes image input as batch_size x Channel x Image width x Image Height .
    plt.imsave("images/dalle2_output.png", images) # finally save your prediction .


if __name__ == '__main__':
    train_model()
    generate_images()
    


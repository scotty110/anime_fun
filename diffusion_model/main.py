'''
Setup an diffusion model behind a twirp server
'''
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
import torch

# Twirp Stuff
import asyncio
import logging

from twirp.context import Context
from twirp.asgi import TwirpASGIApp

import llm_pb2
import llm_twirp


'''
Links:
    https://huggingface.co/stabilityai/stable-diffusion-3.5-large
'''

nf4_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)


class DiffusionService():
    def __init__(self):
        model = 'stabilityai/stable-diffusion-3.5-large'

        self.model = SD3Transformer2DModel.from_pretrained(
                        model,
                        subfolder="transformer",
                        quantization_config=nf4_config,
                        torch_dtype=torch.bfloat16)

        self.pipeline = StableDiffusion3Pipeline.from_pretrained(
                        model, 
                        transformer=self.model,
                        torch_dtype=torch.bfloat16)

        self.pipeline.enable_model_cpu_offload()

    def generate(self, prompt) -> bytes:
        prompt = f'An anime character in the style of Tatsuki Fujimoto with the following characteristics: {prompt}'
        img = self.pipeline(
            prompt=prompt,
            num_inference_steps=28,
            guidance_scale=4.5,
            max_sequence_length=512).images[0]
        return img


class FrierenDiffusion(object):
    def __init__(self):
        print(torch.cuda.is_available())
        self.model = DiffusionService()
        print('Loaded Model')

    def GenBio(self, context, req) -> llm_pb2.AImage:
        s = self.model.generate(req.Text)

        r_obj = llm_pb2.AImage()
        r_obj.Text = s #bytes???
        return r_obj


# Start Server
logging.basicConfig()
service = llm_twirp.GenTextServer(service=FrierenDiffusion())
app = TwirpASGIApp()
app.add_service(service)

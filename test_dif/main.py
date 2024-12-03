'''
Setup an llm behind a twirp server
'''

from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
import torch

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


class DiffusionModel():
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
    
if __name__ == '__main__':
    model = DiffusionModel()
    while True:
        user_input = input("Please enter something (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user enters 'exit'

        # Generate and save image
        t = model.generate(user_input)
        t.save("test.png")
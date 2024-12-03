'''
Setup an llm behind a twirp server
'''

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import transformers
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
    https://huggingface.co/blog/4bit-transformers-bitsandbytes

    https://github.com/Dao-AILab/flash-attention
    https://huggingface.co/docs/transformers/perf_infer_gpu_one

    https://github.com/scotty110/xyz_StableD/tree/master/stable_diffusion

'''



nf4_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)


class LLMService():
    def __init__(self):
        llm = 'meta-llama/Llama-3.2-3B-Instruct'
        self.tokenizer = AutoTokenizer.from_pretrained( llm )

        self.model = AutoModelForCausalLM.from_pretrained( 
                        llm, 
                        quantization_config=nf4_config, 
                        device_map="auto")

        self.pipeline = pipeline(
                            'text-generation', 
                            model=self.model, 
                            tokenizer=self.tokenizer)

    def generate(self, prompt) -> str:
        messages = [
            {"role": "system", "content": "You are famed anime creator Tatsuki Fujimoto. Be concise."}, 
            {"role": "user", "content": f"Create a character using the following information, include a name, physical description, hobbies, personality: {prompt}"},
        ]
        sequences = self.pipeline(
            messages,
            max_new_tokens=256,
            return_full_text=False,
            do_sample=True,
            temperature=0.7,
            top_k=40,
            top_p=0.9,
         )
        return sequences[0]['generated_text']


class FrierenLLM(object):
    def __init__(self):
        print(torch.cuda.is_available())
        self.model = LLMService()
        print('Loaded Model')

    def GenBio(self, context, req) -> llm_pb2.AText:
        s = self.model.generate(req.Text)

        r_obj = llm_pb2.AText()
        r_obj.Text = s
        return r_obj


# Start Server
logging.basicConfig()
service = llm_twirp.GenTextServer(service=FrierenLLM())
app = TwirpASGIApp()
app.add_service(service)

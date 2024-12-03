'''
Setup an llm behind a twirp server
'''

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import transformers
import torch

'''
Links:
    https://huggingface.co/blog/4bit-transformers-bitsandbytes
    https://huggingface.co/docs/transformers/perf_infer_gpu_one

    https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
'''



nf4_config = BitsAndBytesConfig(
   load_in_4bit=True,
   bnb_4bit_quant_type="nf4",
   bnb_4bit_use_double_quant=True,
   bnb_4bit_compute_dtype=torch.bfloat16
)


class ChatLLM():
    def __init__(self):
        llm = 'meta-llama/Llama-3.2-3B-Instruct'
        #llm = 'microsoft/Phi-3.5-mini-instruct'
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


if __name__ == '__main__':
    model = ChatLLM()
    while True:
        user_input = input("Please enter something (or 'exit' to quit): ")
    
        if user_input.lower() == 'exit':
            break  # Exit the loop if the user enters 'exit'
    
        # Do something with the user input
        #print(f'You entered: {user_input}')
        t = model.generate(user_input)
        print(f'Model Output: \n {t}')


'''
Generate a character in the style of Tatsuki Fujimoto based on the following description, giving the character a name if not provided: Girl with blond hair and blue eyes

'''
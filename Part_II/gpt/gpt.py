import os
import pathlib
import torch
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import hf_hub_download, snapshot_download

def download_model(CACHE_DIR = '.hfcache'):
    snapshot_download("EleutherAI/gpt-neo-1.3B", cache_dir=CACHE_DIR)

print('Loading gpt neo...')
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f'using device {device}')

# CDIR = pathlib.Path(__file__).parent.resolve()
# MODEL_DIR = os.path.join(CDIR, r'EleutherAI__gpt-neo-1.3B.main.797174552ae47f449ab70b684cabcb6603e5e85e/')
# model = AutoModelForCausalLM.from_pretrained(MODEL_DIR).to(device)
# tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B").to(device)
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
generator = pipeline(
    'text-generation', 
    model=model, 
    tokenizer=tokenizer, 
    device=0 if torch.cuda.is_available() else -1)



def get_completion(prompt, temperature, stop):
    output = generator(
        prompt, 
        do_sample=True, 
        min_length=50, 
        temperature=temperature, 
        max_length=800,
        return_full_text=False,
        stop=stop)
    return output[0]['generated_text'].split(stop)[0]

from transformers import PreTrainedTokenizerFast
import math
import torch
from tokenizers import Tokenizer
from datasets import load_dataset
from progen.progen2.models.progen.modeling_progen import ProGenForCausalLM
from transformers import PreTrainedTokenizerFast
from Bio import SeqIO
from sklearn import datasets
from datasets import Dataset
from transformers import DataCollatorForLanguageModeling
from tqdm import tqdm
from datetime import datetime

import argparse
parser = argparse.ArgumentParser(
    description="Script for generating sequences using a Progen2 fine tuned model"
)
parser.add_argument("--run_name", required=True, type=str)
parser.add_argument("--model_checkpoint", required=True, type=str)
parser.add_argument("--context", required=True, type=str)
parser.add_argument("--max_length", required=True, type=int)
parser.add_argument("--direction", required=True, type=str)
parser.add_argument("--temperature", required=True, type=float)
parser.add_argument("--p", required=True, type=float)
parser.add_argument("--num_runs", required=True, type=int)
parser.add_argument("--gpu", required=False, type=str, default = 'cuda:0')
args = parser.parse_args()

def create_tokenizer_custom(file):
    with open(file, 'r') as f:
        return Tokenizer.from_str(f.read())

def main():
    run_name = args.run_name
    model_checkpoint = args.model_checkpoint
    context = args.context
    max_length = args.max_length
    direction = args.direction
    temp = args.temperature
    p = args.p
    num_runs = args.num_runs
    gpu = args.gpu

    # Load and set up model
    device = torch.device(gpu if torch.cuda.is_available() else "cpu")
    model = ProGenForCausalLM.from_pretrained(model_checkpoint, torch_dtype=torch.float32).to(device)
    # Assuming 'model' is your model variable
    is_on_cuda = next(model.parameters()).is_cuda
    print(is_on_cuda)
    # Create tokenizer for generating sequences
    tokenizer = create_tokenizer_custom(file='progen/progen2/tokenizer.json')
    tokenizer.save("my-tokenizer.json")
    fast_tokenizer = PreTrainedTokenizerFast(tokenizer_file="my-tokenizer.json")
    fast_tokenizer.eos_token = '<|eos|>'
    fast_tokenizer.pad_token = fast_tokenizer.eos_token
    # Generate sequences:
    fasta_filename = run_name + "_sequences.fasta"
    if direction == 'reverse':
        prompt_rev = '1'+context[::-1]
        print('context: ' + prompt_rev)
        input_ids = torch.tensor(fast_tokenizer.encode(prompt_rev)).view([1, -1]).to(device)
        j=0
        for i in tqdm(range(num_runs)):
            tokens_batch = model.generate(input_ids, do_sample=True, temperature=temp, max_length=max_length, top_p=p, num_return_sequences=20, pad_token_id=0)
            as_lists = lambda batch: [batch[i, ...].detach().cpu().numpy().tolist() for i in range(batch.shape[0])]
            sequences = tokenizer.decode_batch(as_lists(tokens_batch))
            # Write sequences to a FASTA file
            with open(fasta_filename, 'a') as fasta_file:
                for sequence in sequences:
                    # Remove 2 at the end if it exists
                    if sequence.endswith('2'):
                        sequence = sequence[:-1]
                    sequence = sequence[::-1]
                    fasta_file.write('>' + run_name + f'_seq{j}\n')
                    fasta_file.write(sequence[:-1] + '\n')
                    j += 1
    else: 
        prompt = '1' + context
        print('context: ' + prompt)
        input_ids = torch.tensor(fast_tokenizer.encode(prompt)).view([1, -1]).to(device)
        j=0
        for i in tqdm(range(num_runs)):
            tokens_batch = model.generate(input_ids, do_sample=True, temperature=temp, max_length=max_length, top_p=p, num_return_sequences=20, pad_token_id=0)
            as_lists = lambda batch: [batch[i, ...].detach().cpu().numpy().tolist() for i in range(batch.shape[0])]
            sequences = tokenizer.decode_batch(as_lists(tokens_batch))
            # Write sequences to a FASTA file
            with open(fasta_filename, 'a') as fasta_file:
                for sequence in sequences:
                    # Remove 2 at the end if it exists
                    if sequence.endswith('2'):
                        sequence = sequence[:-1]
                    fasta_file.write('>' + run_name + f'_seq{j}\n')
                    fasta_file.write(sequence[1:] + '\n')
                    j += 1


if __name__ == "__main__":
    main()
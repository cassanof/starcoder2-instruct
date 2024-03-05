import datasets
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=True)
parser.add_argument('--push', action='store_true')
args = parser.parse_args()


incomplete_substrings = [
    "todo",
    "fixme",
    "write your code here",
    "your code here",
    "your code goes here",
    "notimplemented",
]


def filter_fn(example):
    lowered = example["solution"].lower()
    return not any(substring in lowered for substring in incomplete_substrings)


dataset = datasets.load_dataset(args.dataset, split="train")
dataset = dataset.filter(
    filter_fn,
    num_proc=os.cpu_count(),
)
dataset.push_to_hub(args.push, private=True)

import datasets
import pandas as pd
from typing import Callable, Dict, Optional, Tuple

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--push", type=str, required=True)
parser.add_argument("--mark", type=str, default="")
args = parser.parse_args()

ExampleTransform = Callable[[dict], str]
DatasetGetter = Callable[[], datasets.Dataset]


def add_markdown_code_block(s: str, tag) -> str:
    return f"```{tag}\n{s}\n```"


# <ds getter> -> (<context block>, <instruction>, <code block>, <lang>)
DATASETS = {
    (lambda: datasets.load_dataset("bigcode/self-oss-instruct-sc2-exec-filter-50k", split="train")): (  # type: ignore
        lambda _: None,
        lambda x: x["instruction"],
        lambda x: x["response"],
        lambda _: "python",
        "oss-instruct-sc2"
    ),
}


def format_prompt(context: Optional[str], instruction: str, code: str) -> str:
    context_header = "# Context"
    instruction_header = "# Instruction"
    response_header = "# Response"
    buf = ""
    if context is not None:
        buf += context_header + "\n"
        buf += context + "\n"
    buf += instruction_header + "\n"
    buf += instruction + "\n"
    buf += response_header + "\n" + args.mark
    buf += code + "\n"
    return buf


def process_ex(ex, context, instruction, code, lang, from_ds):
    ex["context"] = context(ex)
    ex["instruction"] = instruction(ex)
    ex["code"] = code(ex)
    ex["lang"] = lang(ex)
    ex["from_ds"] = from_ds
    ex["content"] = format_prompt(
        ex["context"], ex["instruction"], ex["code"])
    return ex


FINAL = []
for ds, (context, instruction, code, lang, from_ds) in DATASETS.items():
    raw = ds()
    print(raw)
    raw = raw.map(lambda x: process_ex(
        x, context, instruction, code, lang, from_ds))
    # print distribution of lang
    df = pd.DataFrame(raw["lang"])
    df.columns = ["lang"]
    # TODO: may need to downsample YAML+JSON+HTML for EditPackFT, or maybe not :shrug:
    print(df.describe())
    FINAL.extend(raw)

FINAL = datasets.Dataset.from_list(FINAL).shuffle()
print(len(FINAL))

# print some examples of "content"
for i in range(3):
    print(FINAL[i]["content"])

FINAL.push_to_hub(args.push, private=True)

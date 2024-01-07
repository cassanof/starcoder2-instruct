import datasets
from typing import Callable, Dict, Tuple

ExampleTransform = Callable[[dict], str]
DatasetGetter = Callable[[], datasets.Dataset]


def add_markdown_code_block(s: str, tag="python") -> str:
    return f"```{tag}\n{s}\n```"


# <ds getter> -> (<context block>, <instruction>, <code block>)
DATASETS: Dict[DatasetGetter, Tuple[ExampleTransform, ExampleTransform, ExampleTransform]] = {
    (lambda: datasets.load_dataset("nuprl/EditPackFT", split="train[:100000]")): ( # type: ignore
        lambda x: add_markdown_code_block(x["old_contents"]),
        lambda x: x["instruction"],
        lambda x: x["new_contents"],
    ),
}

from human_eval.evaluation import evaluate_functional_correctness
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.utils import extract_generation_code, languge_settings
import argparse
import json
import os
import torch
from pathlib import Path
from tqdm import tqdm

data_abs_dir = Path(__file__).parent / "data"


def build_instruction(languge: str, question: str):
    return '''
Please continue to complete the function. You are not allowed to modify the given code, and you are allowed to only complete it. Please return the completed function in a codeblock. Here is the given code to complete:
```{}
{}
```
'''.strip().format(languge.lower(), question.strip())


def format_prompt(instruction: str, prompt: str, lang: str) -> str:
    instruction_header = "# Instruction"
    response_header = "# Response"
    buf = ""
    buf += instruction_header + "\n"
    buf += instruction + "\n"
    buf += response_header + "\n"
    buf += f"""```{lang.lower()}
{prompt}""".strip()
    return buf


def generate_one(example, lang, tokenizer, model):
    instr = build_instruction(
        languge_settings[lang]['full_name'], example['prompt'])
    prompt = format_prompt(
        instr, example['prompt'], languge_settings[lang]['full_name'])
    print(prompt)
    inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        inputs,
        max_new_tokens=1024,
        do_sample=False,
        # top_p=0.9,
        # temperature=0.2,
        # do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    print("------ RAW --------")
    output = tokenizer.decode(
        outputs[0], skip_special_tokens=True)
    output = output.split("# Response")[1].strip()
    print(output)
    example['output'] = output

    ext = extract_generation_code(example, lang_code=lang)
    print("------ EXTRACTED --------")
    print(ext["generation"])
    return ext


def generate_main(args):
    model_name_or_path = args.model
    lang = args.language
    saved_path = args.output_path
    temp_dir = args.temp_dir
    os.makedirs(temp_dir, exist_ok=True)
    problem_file = os.path.join(data_abs_dir, f"humaneval-{lang}.jsonl")

    print("model", model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    print("load tokenizer {} from {} over.".format(
        tokenizer.__class__, model_name_or_path))
    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        # use_flash_attention_2=True
    )
    model.eval()
    examples = [json.loads(x) for x in open(problem_file) if x.strip()]
    print("Read {} examples for evaluation over.".format(len(examples)))

    generated_examples = []
    for ex in tqdm(examples, desc='Generating'):
        gen_example = generate_one(ex, args.language, tokenizer, model)
        generated_examples.append(gen_example)

    print("Generate all over!!!")
    with open(saved_path, 'w', encoding='utf-8') as fw:
        for ex in generated_examples:
            fw.write(json.dumps(ex) + '\n')
        print("Save {} processed examples into {} over!".format(
            len(generated_examples), saved_path))

    result = evaluate_functional_correctness(
        input_file=saved_path,
        tmp_dir=temp_dir,
        n_workers=8,
        timeout=3.0,
        problem_file=problem_file,
        language=lang
    )
    print(lang, result, model_name_or_path)
    pass


def evaluation_only(args):
    lang = args.language
    temp_dir = args.temp_dir
    assert os.path.exists(
        args.output_path), "Not fond output file: {}".format(args.output_path)
    os.makedirs(temp_dir, exist_ok=True)

    output_name = os.path.basename(args.output_path)
    output_examples = [json.loads(x)
                       for x in open(args.output_path) if x.strip()]

    processed_examples = [extract_generation_code(
        ex, lang) for ex in tqdm(output_examples, "Processing")]
    processed_path = os.path.join(temp_dir, output_name)
    with open(processed_path, 'w', encoding='utf-8') as fw:
        for ex in processed_examples:
            fw.write(json.dumps(ex) + '\n')
        print("Save {} processed examples into {} over!".format(
            len(processed_examples), processed_path))

    problem_file = os.path.join(data_abs_dir, f"humaneval-{lang}.jsonl")
    from human_eval.evaluation import evaluate_functional_correctness
    result = evaluate_functional_correctness(
        input_file=processed_path,
        tmp_dir=temp_dir,
        n_workers=8,
        timeout=3.0,
        problem_file=problem_file,
        language=lang
    )
    print(lang, result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, help="model name or path")
    parser.add_argument('--output_path', type=str,
                        help="output path of your generation")
    parser.add_argument('--language', type=str, help="langauge")
    parser.add_argument('--temp_dir', type=str,
                        help="temp dir for evaluation", default="tmp")
    args = parser.parse_args()

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    generate_main(args)
    pass

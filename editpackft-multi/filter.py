import datasets
from tqdm import tqdm
import editdistance
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--push", type=str, required=True,
                    help="HuggingFace repo to push to")
args = parser.parse_args()

configs = ['abap', 'actionscript', 'ada', 'agda', 'antlr', 'apacheconf', 'api-blueprint', 'apl', 'applescript', 'arc', 'arduino', 'asciidoc', 'asp', 'aspectj', 'assembly', 'ats', 'augeas', 'autohotkey', 'awk', 'batchfile', 'bitbake', 'blitzmax', 'bluespec', 'boo', 'brainfuck', 'bro', 'c', 'c#', 'c++', 'c2hs-haskell', 'capn-proto', 'cartocss', 'ceylon', 'chapel', 'clean', 'clojure', 'cmake', 'coffeescript', 'coldfusion', 'coldfusion-cfc', 'common-lisp', 'creole', 'crystal', 'csound', 'css', 'csv', 'cucumber', 'cuda', 'cython', 'dart', 'desktop', 'diff', 'digital-command-language', 'dm', 'dns-zone', 'dockerfile', 'dylan', 'eagle', 'ecl', 'edn', 'eiffel', 'elixir', 'elm', 'emacs-lisp', 'emberscript', 'erlang', 'f#', 'factor', 'fancy', 'fish', 'flux', 'forth', 'fortran', 'freemarker', 'g-code', 'gas', 'gdscript', 'genshi', 'gentoo-ebuild', 'gettext-catalog', 'glsl', 'gnuplot', 'go', 'graphql', 'graphviz-dot', 'groff', 'groovy', 'groovy-server-pages', 'haml', 'handlebars', 'harbour', 'haskell', 'haxe', 'hcl', 'hlsl', 'html', 'html+django', 'html+eex', 'html+erb', 'html+php', 'http', 'hy', 'idris', 'igor-pro', 'inform-7', 'ini', 'inno-setup', 'io', 'ioke',
           'isabelle', 'jade', 'jasmin', 'java', 'java-server-pages', 'javascript', 'jflex', 'json', 'json5', 'jsoniq', 'jsonld', 'jsx', 'julia', 'jupyter-notebook', 'kotlin', 'krl',
           'latte', 'lean', 'less', 'lfe', 'lilypond', 'linker-script', 'liquid', 'literate-agda', 'literate-coffeescript', 'literate-haskell', 'livescript', 'llvm', 'logos', 'logtalk', 'lsl', 'lua', 'm4', 'makefile', 'mako', 'maple', 'markdown', 'mask', 'mathematica', 'mediawiki', 'metal', 'mirah', 'modelica', 'module-management-system', 'monkey', 'moonscript', 'mtml', 'mupad', 'nesc', 'netlinx', 'nginx', 'nimrod', 'ninja', 'nit', 'nix', 'nsis', 'nu', 'objective-c++', 'ocaml', 'ooc', 'opencl', 'openscad', 'org', 'oz', 'pan', 'parrot-assembly', 'parrot-internal-representation', 'pascal', 'pawn', 'perl', 'perl6', 'php', 'piglatin', 'pike', 'pod', 'pony', 'postscript', 'pov-ray-sdl', 'powershell', 'processing', 'propeller-spin', 'protocol-buffer', 'pure-data', 'purebasic', 'purescript', 'python', 'qmake', 'qml', 'r', 'racket', 'ragel-in-ruby-host', 'raml', 'rdoc', 'rebol', 'red', 'renpy', 'restructuredtext', 'rhtml', 'robotframework', 'rouge', 'ruby', 'rust', 'sage', 'saltstack', 'sas', 'sass', 'scala', 'scaml', 'scheme', 'scilab', 'scss', 'shell', 'slash', 'slim', 'smalltalk', 'smarty', 'smt', 'solidity', 'sourcepawn', 'sparql', 'sqf', 'sql', 'squirrel', 'standard-ml', 'stata', 'ston', 'stylus', 'supercollider', 'svg', 'swift', 'systemverilog', 'tcl', 'tcsh', 'tex', 'text', 'textile', 'thrift', 'toml', 'turtle', 'twig', 'typescript', 'unity3d-asset', 'unknown', 'uno', 'unrealscript', 'urweb', 'vala', 'vcl', 'vhdl', 'viml', 'visual-basic', 'volt', 'vue', 'webidl', 'wisp', 'xbase', 'xml', 'xpages', 'xproc', 'xquery', 'xs', 'xslt', 'xtend', 'yacc', 'yaml', 'yang', 'zephir', 'zig']

all_exs = []
for c in tqdm(configs, total=len(configs)):
    try:
        ds = datasets.load_dataset("bigcode/commitpackft", c, split="train")
    except:
        continue
    for ex in ds:
        ex["config"] = c
        all_exs.append(ex)




def cleanup(code):
    lines = code.split("\n")
    d = 0
    in_docstring = False
    for i, l in enumerate(lines):
        dsc = l.count('"""')
        if dsc == 1:
            if in_docstring:
                d = i + 1
                break
            else:
                in_docstring = True
        elif not in_docstring and l.startswith("#"):
            d = i + 1
        elif not in_docstring and l.strip() != "":
            break

    return "\n".join(lines[d:])


exs = []
blanks = 0
no_diff = 0
bad_comments = 0
syntax_errors = 0
badwords = ["TODO", "FIXME", "BUG", "FIX ME"]
badwords_lower = [b.lower() for b in badwords]
badwords.extend(badwords_lower)
for ex in tqdm(all_exs, total=len(all_exs)):
    ex["new_contents"] = cleanup(ex["new_contents"])
    ex["old_contents"] = cleanup(ex["old_contents"])
    # TODO: maybe we want to keep these?
    if ex["old_contents"].strip() == "" or ex["new_contents"].strip() == "":
        blanks += 1
        continue

    skip = False
    for b in badwords:
        if b in ex["new_contents"]:
            skip = True
            break

    if skip:
        bad_comments += 1
        continue

    dist = editdistance.eval(ex["old_contents"], ex["new_contents"])
    if dist < 10:
        no_diff += 1
        continue

    # TODO: for popular langs, we should check for syntax errors using tree-sitter
    #  try:
        #  ast.parse(ex["new_contents"])
    #  except:
        #  syntax_errors += 1
        #  continue

    exs.append(ex)

print("blanks", blanks)
print("no_diff", no_diff)
print("bad_comments", bad_comments)
print("syntax_errors", syntax_errors)
print("no_diff", no_diff)
print("size", len(exs))
new_ds = datasets.Dataset.from_list(exs)
new_ds.push_to_hub(args.push, private=True)

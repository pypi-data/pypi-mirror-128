from typing import Optional
from .utils.datatypes import Index

from pathlib import Path

import re
import click
from click_default_group import DefaultGroup

def get_files(directory):
    files = directory.rglob( "**/*.kam")
    split_list = Index()

    for f in files:
        split_list[f.stem[0] == "_"].add(f) 

    return split_list[0], split_list[1]

def parse_file(file, suple, already=None):

    importing = []
    out_lines = []

    if already == None:
        already = []

    with open(file) as f:
        text = f.read().split("\n")
        
        for line in text:
            if line and line[0] == "@":
                if line.find("import") == 1:
                    path = re.findall('"(.*?)"', line)[0]
                    
                    for x in suple:
                        if (x.parent / x.stem[1:]).as_posix() == path:
                            if x not in already:
                                importing.append(x)
                                already.append(x)
                            break
                    else:
                        raise ValueError(f"Invalid Import: {line}")
                else:
                    raise ValueError(f"Invalid Import Statment: {line}")
            else:
                out_lines.append(line)
        
    for importe in importing:
        out_lines += parse_file(importe, suple, already)

    return out_lines

@click.command(name="compile")
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True), required=False)
def compile_code(directory):

    directory = Path(directory if directory else ".")

    base, suple = get_files(directory)

    for file in base:
        out = "\n".join(parse_file(file, suple))

        with open(f"{str(file)[:-4]}.txt", "w") as f:
            f.write(out)

@click.group(
    cls=DefaultGroup,
    default="compile",
    help="Compliles KAMS to effect lang",
)
def main():
    pass

main.add_command(compile_code)

if __name__ == '__main__':
    main()

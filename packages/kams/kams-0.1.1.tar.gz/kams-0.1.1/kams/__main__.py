from typing import Optional
from .utils.datatypes import Index

from glob import glob
import re
import click
from click_default_group import DefaultGroup

def get_files():#file):
    files = glob( "**/*.kam", recursive=True)

    split_list = Index()

    for f in files:
        split_list['_' in f].add(f) 

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
                        if x.replace("_", "").replace("\\", "/").replace(".kam", "") == path:
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
#@click.argument('file', type=click.Path(exists=True), required=False)
def compile_code():#file):
    #get_config()
    #if not file:
    #    file = '.'

    base, suple = get_files()#file)


    for file in base:
        out = "\n".join(parse_file(file, suple))

        with open(f"{file[:-4]}.txt", "w") as f:
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

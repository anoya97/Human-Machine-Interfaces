#!/usr/bin/env python3

import re
import requests
import sys
import textwrap
from typing import Iterator, NamedTuple, Sequence


URL="https://cheat.sh/"


ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def escape_ansi(line: str):
    return ANSI_ESCAPE.sub('', line)


class CheatEntry(NamedTuple):
    mark: str
    description: str
    commands: str
    tags: str

    def __str__(self) -> str:
        tags = "" if self.tags == "" else f"tags: {self.tags} "
        return f"({self.mark}) {tags}{self.description}\n{self.commands}".strip()

    
def parse_text(text: str) -> list[CheatEntry]:
    default_mark = ""
    recipes = []
    # split("\n\n") splits on blank lines.
    # :warning: Doesn't work for two consecutive blank lines
    for chunk in text.split("\n\n"):
        entry = parse_chunk(chunk)
        if entry.mark == "":
            entry = entry._replace(mark= default_mark)
        elif entry.mark.startswith("cheat"):
            default_mark = entry.mark
        recipes.append(entry)
    return recipes


def parse_chunk(chunk: str) -> CheatEntry:
    mark = ""
    tags = ""
    description = []
    commands = []
    for line in chunk.splitlines():
        if line.startswith(" "):
            mark = line.strip()
        elif line.startswith("#"):
            description.append(line[1:])
        elif line == "---":
            # Asumimos que siempre es sintácticamente correcto
            # TODO: parsear esta especie the frontmatter
            pass
        elif line.startswith("tags: "):
            tags = line.removeprefix("tags: ")
        else:
            commands.append(line)
    return CheatEntry(
        mark= mark,
        description= "\n".join(description), 
        commands= "\n".join(commands),
        tags= tags
    )


def get_cheatsheet(command: str) -> Sequence[CheatEntry]:
    try:
        r = requests.get(URL + command, timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        return "NoRed"

    text = escape_ansi(r.text)
    if text.startswith("Unknown topic."):
        return []
    else:
        return parse_text(text)
    

def takeText(command: str) -> str:

    r = requests.get(URL + command)
    return escape_ansi(r.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} command")
        sys.exit(0)
    
    command_name = sys.argv[1]
    recipes = get_cheatsheet(command_name)
    for i, r in enumerate(recipes, start= 1):
        idx = f"{i}."
        print(
            textwrap.indent(
                f"{idx} {r}",
                prefix= "    ",
                predicate= lambda line: not line.startswith(idx)
            )
        )
        print()

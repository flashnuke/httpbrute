from typing import List
from .output_methods import *


def load_wordlist(path: str) -> List[str]:
    print_info(f"attempting to load wordlist -> {path}")
    wl = list()
    try:
        with open(path, "r", encoding="utf-8") as wordlist:
            parsed = wordlist.readlines()
            for word in parsed:
                wl.append(word.strip("\n"))
    except Exception as exc:
        pass
    return wl


def has_one(iterrable):
    return sum(bool(e) for e in iterrable) == 1

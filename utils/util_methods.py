from typing import List
from .output_methods import *


def load_wordlist(path: str) -> List[str]:
    print_info(f"loading wordlist, path -> {path}")
    wl = list()
    try:
        with open(path, "r") as wordlist:
            parsed = wordlist.readlines()
            for word in parsed:
                wl.append(word.strip("\n"))
    except Exception as exc:
        print_error(f"loading wordlist exception - {exc}")
    return wl


def has_one(iterrable):
    return sum(bool(e) for e in iterrable) == 1


def format_time(elapsed: float) -> str:
    return f"{int(elapsed)}:{60 * elapsed % 60}"

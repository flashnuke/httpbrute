import os
from typing import List
from .output_methods import *


def load_wordlist(path: str) -> List[str]:
    print_info(f"loading wordlist | path -> {path}")
    wl = list()
    try:
        with open(path, "r", encoding='utf8', errors='ignore') as wordlist:
            parsed = wordlist.readlines()
            for word in parsed:
                wl.append(word.strip("\n"))
    except Exception as exc:
        print_error(f"loading wordlist exception - {exc}")
    except KeyboardInterrupt:
        os.kill(os.getpid(), 9)
    return wl


def has_one(iterrable):
    return sum(bool(e) for e in iterrable) == 1


def format_time(elapsed: float) -> str:
    minutes = f"{int(elapsed)}".rjust(2, '0')
    seconds = f"{int((60 * elapsed) % 60)}".rjust(2, '0')
    return f"{minutes}:{seconds}"

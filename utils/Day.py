from requests import get

from pathlib import (Path)

from utils import cookies


def get_data(day: int) -> str:
    file = Path(f"data/day{day}")
    if file.exists():
        return file.open().read()
    r = get(f"https://adventofcode.com/2024/day/{day}/input", cookies=cookies)
    r.raise_for_status()
    with open(Path(f"data/day{day}"), 'w') as f:
        f.write(r.text)
    return r.text

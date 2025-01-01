from requests import get

from pathlib import Path

from src.utils import cookies


def get_data(year: int, day: int) -> str:
    file = Path(f"data/day{day}")
    if file.exists():
        return file.open().read()
    r = get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    r.raise_for_status()
    with open(Path(f"data/day{day}"), "w") as f:
        f.write(r.text)
    return r.text

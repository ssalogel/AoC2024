from src import years
from time import perf_counter
import logging

logger = logging.getLogger("AoC")
logger.setLevel(logging.WARNING)

start = perf_counter()
times = {}
for year, days in years:
    times[year] = {}
    start_year = perf_counter()
    for num, day in enumerate(days):
        times[year][num] = day()

    logger.error(f"{year} ran in {perf_counter() - start_year:.4f} seconds")
print(f"All of AoC ran in {perf_counter() - start:.4f} seconds")

from src import years
from time import perf_counter

start = perf_counter()
for year, days in years:
    start_year = perf_counter()
    for day in days:
        day()

    print(f"year {year} ran in {perf_counter() - start_year} seconds")
print(f"All of AoC ran in {perf_counter() - start} seconds")

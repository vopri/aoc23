from itertools import combinations
from pathlib import Path


class Universe:
    def __init__(self, file_name: str, first_index_1=True):
        self.array = self._parse(file_name)
        self._index_offset = 1 if first_index_1 else 0
        self._expand()

    def _parse(self, file_name: str) -> list[str]:
        return Path(file_name).read_text().splitlines()

    def _expand(self):
        self._expand_rows()
        self._expand_cols()

    def _expand_rows(self):
        offset = 0
        local_array = self.array.copy()
        for row_idx, row in enumerate(local_array):
            if self._is_empty(row):
                self.array.insert(row_idx + offset, row)
                offset += 1

    def _expand_cols(self):
        empty_cols = self._get_empty_cols()
        for row_idx, row in enumerate(self.array):
            offset = 0
            for col in empty_cols:
                row = row[: col + offset] + "." + row[col + offset :]
                self.array[row_idx] = row
                offset += 1

    def _get_empty_cols(self):
        return [
            col_idx
            for col_idx in range(len(self.array[0]))
            if self._is_empty(self.get_col(col_idx + self._index_offset))
        ]

    def get(self, col_idx: int, row_idx: int) -> str:
        row = self.array[row_idx - self._index_offset]
        return row[col_idx - self._index_offset]

    def get_row(self, row_idx: int) -> str:
        return self.array[row_idx - self._index_offset]

    def get_col(self, col_idx: int) -> str:
        return "".join(
            [
                symbol
                for row in self.array
                for symbol in row[col_idx - self._index_offset]
            ]
        )

    def find_galaxies(self) -> list[tuple[int, int]]:
        galaxies = []
        for row_idx, row in enumerate(self.array):
            for col_idx, symbol in enumerate(row):
                if symbol == "#":
                    galaxies.append(
                        (col_idx + self._index_offset, row_idx + self._index_offset)
                    )
        return galaxies

    def get_distance_between_galaxies(
        self, galaxy_1: tuple[int, int], galaxy_2: tuple[int, int]
    ) -> int:
        return abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])

    def _is_empty(self, row_or_col: str) -> bool:
        for symbol in row_or_col:
            if symbol != ".":
                return False
        return True

    def __str__(self):
        return "\n".join([row for row in self.array])


file = "11/test_input.txt"
file = "11/input.txt"
universe = Universe(file)
galaxy_pairs = combinations(universe.find_galaxies(), 2)
sum_of_galaxy_distances = sum(
    [universe.get_distance_between_galaxies(g1, g2) for g1, g2 in galaxy_pairs]
)
print("Part 1:", sum_of_galaxy_distances)

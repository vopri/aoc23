from itertools import combinations
from pathlib import Path


class Universe:
    def __init__(self, file_name: str, first_index_1=True, part_1=True):
        self.array = self._parse(file_name)
        self._factor = 1 if part_1 else 1_000_000 - 1
        self._index_offset = 1 if first_index_1 else 0
        self._empty_rows = self._get_empty_rows_using_offset()
        self._empty_cols = self._get_empty_cols_using_offset()

    def _parse(self, file_name: str) -> list[str]:
        return Path(file_name).read_text().splitlines()

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
        non_expanded_space = abs(galaxy_1[0] - galaxy_2[0]) + abs(
            galaxy_1[1] - galaxy_2[1]
        )
        return (
            non_expanded_space
            + self._get_additional_empty_space_steps_bettween_two_galaxies(
                galaxy_1, galaxy_2
            )
        )

        return non_expanded_space

    def _is_empty(self, row_or_col: str) -> bool:
        for symbol in row_or_col:
            if symbol != ".":
                return False
        return True

    def _get_empty_cols_using_offset(self):
        return [
            col_idx
            for col_idx in range(
                self._index_offset, len(self.array[0]) + self._index_offset
            )
            if self._is_empty(self.get_col(col_idx))
        ]

    def _get_empty_rows_using_offset(self):
        return [
            row_idx
            for row_idx, row in enumerate(self.array, self._index_offset)
            if self._is_empty(self.get_row(row_idx))
        ]

    def _get_additional_empty_space_steps_bettween_two_galaxies(
        self, g1: tuple[int, int], g2: tuple[int, int]
    ) -> int:
        # minus 1, because it's additional

        counter = 0
        x1, y1 = g1
        x2, y2 = g2
        for empty_row in self._empty_rows:
            if empty_row > min((y1, y2)) and empty_row < max((y1, y2)):
                counter += 1
        for empty_col in self._empty_cols:
            if empty_col > min((x1, x2)) and empty_col < max((x1, x2)):
                counter += 1
        return counter * self._factor

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

# part 2
universe = Universe(file, part_1=False)
universe._factor
galaxy_pairs = combinations(universe.find_galaxies(), 2)
sum_of_galaxy_distances = sum(
    [universe.get_distance_between_galaxies(g1, g2) for g1, g2 in galaxy_pairs]
)
print("Part 2:", sum_of_galaxy_distances)

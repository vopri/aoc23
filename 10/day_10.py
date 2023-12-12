import sys
from math import floor
from pathlib import Path

# default recursion depth too low for this puzzle
sys.setrecursionlimit(15000)


class ElvenGraph:
    def __init__(self, file: str):
        self._content: str = Path(file).read_text()
        self._line_len = self._content.find("\n")
        self.start_idx: int = self._content.find("S")

    def get_neighbours(self, idx: int) -> list[int]:
        symbol = self._content[idx]
        neigbhours = []
        if symbol in ("S", "|", "L", "J"):
            neigbhours.append(graph._above(idx))
        if symbol in ("S", "7", "F", "|"):
            neigbhours.append(graph._below(idx))
        if symbol in ("S", "-", "J", "7"):
            neigbhours.append(graph._left(idx))
        if symbol in ("S", "L", "F", "-"):
            neigbhours.append(graph._right(idx))
        return [neigbhour for neigbhour in neigbhours if neigbhour is not None]

    def count_steps_max_distance_loop(self) -> int:
        def depth_first_trav(idx: int, parent_idx: int):
            visited.append(idx)
            for neigbhour_idx in self.get_neighbours(idx):
                if neigbhour_idx == parent_idx:
                    continue
                if neigbhour_idx in visited:
                    return
                depth_first_trav(neigbhour_idx, idx)

        visited = []
        depth_first_trav(self.start_idx, -1)
        return floor(len(visited) / 2)

    #### private stuff ####

    def _left(self, idx: int) -> int | None:
        if idx == 0:
            return None
        else:
            result = idx - 1
            return result if self._is_pipe(result) else None

    def _right(self, idx: int) -> int | None:
        if idx == len(self._content) - 1:
            return None
        else:
            result = idx + 1
            return result if self._is_pipe(result) else None

    def _above(self, idx: int) -> int | None:
        result = idx - self._line_len - 1
        if result < 0:
            return None
        else:
            return result if self._is_pipe(result) else None

    def _below(self, idx: int) -> int | None:
        result = idx + self._line_len + 1
        if result > len(self._content) - 1:
            return None
        else:
            return result if self._is_pipe(result) else None

    def _is_pipe(self, idx: int) -> bool:
        return self._content[idx] not in ("\n", ".")


graph = ElvenGraph("10/test_input.txt")
graph = ElvenGraph("10/input.txt")
print("Part 1:", graph.count_steps_max_distance_loop())

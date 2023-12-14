import sys
from itertools import batched, islice, pairwise
from math import floor, log10
from pathlib import Path

from rich.console import Console

# default recursion depth too low for this puzzle
sys.setrecursionlimit(15000)


class ElvenGraph:
    def __init__(self, file: str):
        self._content: str = Path(file).read_text()
        self._line_len = self._content.find("\n")
        self.start_idx: int = self._content.find("S")
        self.loop = []
        self._enclosed_tiles = []

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
            self.loop.append(idx)
            for neigbhour_idx in self.get_neighbours(idx):
                if neigbhour_idx == parent_idx:
                    continue
                if neigbhour_idx in self.loop:
                    return
                depth_first_trav(neigbhour_idx, idx)

        depth_first_trav(self.start_idx, -1)
        return floor(len(self.loop) / 2)

    def print_pipe(self):
        if self.loop is None:
            self.count_steps_max_distance_loop()
        console = Console()
        for index, char in enumerate(self._content):
            if index in self.loop:
                if char == "S":
                    console.print(char, style="white on green", end="")
                else:
                    match char:
                        case "F":
                            replaced_char = "\u250c"
                        case "J":
                            replaced_char = "\u2518"
                        case "L":
                            replaced_char = "\u2514"
                        case "7":
                            replaced_char = "\u2510"
                        case _:
                            replaced_char = char
                    console.print(
                        replaced_char,
                        style="white on red",
                        end="",
                    )
            elif index in self._enclosed_tiles:
                console.print(char, style="black on yellow", end="")
            elif char == "\n":
                console.print()
            else:
                console.print(char, end="")

    def count_enclosed_pipes(self):
        counts = []
        for line_no, _ in enumerate(self._content.splitlines()):
            for open, closed in batched(
                self._extract_vertical_pipes_in_line_sorted_by_idx(line_no), n=2
            ):
                counted_symbols_between_pipes = closed - open - 1
                if counted_symbols_between_pipes == 0:
                    continue
                potential_hits = range(open + 1, closed)
                for potential_hit_idx in potential_hits:
                    if potential_hit_idx in self.loop:
                        continue
                    else:
                        counts.append(1)
                        self._enclosed_tiles.append(potential_hit_idx)
        return len(self._enclosed_tiles)

    def _extract_vertical_pipes_in_line_sorted_by_idx(self, line_no: int) -> list[int]:
        VERTICAL = "S F | 7 ".split()
        if not hasattr(self, "_vertical_pipe_idxs"):
            self._vertical_pipe_idxs = sorted(
                [idx for idx in self.loop if self._content[idx] in VERTICAL]
            )
        from_ = line_no * self._line_len + line_no
        until = from_ + self._line_len + 1
        result = [
            idx for idx in self._vertical_pipe_idxs if idx >= from_ and idx < until
        ]
        return result

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


# graph = ElvenGraph("10/test_2_input.txt")
# graph = ElvenGraph("10/test_3_input.txt")
# graph = ElvenGraph("10/test_4_input.txt")
graph = ElvenGraph("10/input.txt")
print("Part 1:", graph.count_steps_max_distance_loop())

print("Part 2:", graph.count_enclosed_pipes())
# graph.print_pipe()

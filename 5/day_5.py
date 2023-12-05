from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class MappingRange:
    # e.g. 50 98 2
    destination_start: int
    source_start: int
    range: int

    def get_destination(self, source: int) -> int | None:
        if (source >= self.source_start) and (
            source <= self.source_start + self.range - 1
        ):
            offset = source - self.source_start
            return self.destination_start + offset
        else:
            return None


@dataclass
class Mapping:
    # e.g. seed-to-soil map
    name: str
    mapping_ranges: set[MappingRange] = field(init=False, default_factory=set)

    def add(self, mapping: MappingRange):
        self.mapping_ranges.add(mapping)

    def __getitem__(self, source: int) -> int:
        for mapping in self.mapping_ranges:
            dest = mapping.get_destination(source)
            if dest is not None:
                return dest
        return source


class Almanac:
    # assumption: Mappings come in order as needed => list
    def __init__(self, seeds: list[int]):
        self.seeds = seeds
        self._mappings: list[Mapping] = []

    def add(self, mapping: Mapping):
        self._mappings.append(mapping)

    def find_location(self, seed: int) -> int:
        src = seed
        for mapping in self._mappings:
            # assumpiton: last map is location
            src = mapping[src]
        return src

    def find_seed_with_lowest_location(self) -> tuple[int, int]:
        location_to_seed = {self.find_location(seed): seed for seed in self.seeds}
        min_location = min(location_to_seed.keys())
        return min_location, location_to_seed[min_location]


def parse(file: str) -> Almanac:
    content = Path(file).read_text().splitlines()
    seeds = [int(seed) for seed in content[0].split(": ")[1].split()]
    almanac = Almanac(seeds)
    for line in content[1:]:
        match (line.split()):
            case []:
                continue
            case [name, *garbage] if not name[0].isdigit():
                mapping = Mapping(name)
                almanac.add(mapping)
            case [dest_start, src_start, range]:
                mr = MappingRange(int(dest_start), int(src_start), int(range))
                mapping.add(mr)  # type: ignore
            case _:
                raise RuntimeError("Unexpected!")
    return almanac


file = "5/input.txt"
almanac = parse(file)
lowest_location, seed = almanac.find_seed_with_lowest_location()
print(f"Part 1: Lowest location is {lowest_location} for initial seed {seed}")

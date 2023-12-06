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

    def get_source(self, destination: int) -> int | None:
        if (destination >= self.destination_start) and (
            destination <= self.destination_start + self.range - 1
        ):
            offset = destination - self.destination_start
            return self.source_start + offset
        else:
            return None


@dataclass
class Mapping:
    # e.g. seed-to-soil map
    name: str
    mapping_ranges: list[MappingRange] = field(init=False, default_factory=list)

    def add(self, mapping: MappingRange):
        self.mapping_ranges.append(mapping)

    def get_destination(self, source: int) -> int:
        for mapping in self.mapping_ranges:
            dest = mapping.get_destination(source)
            if dest is not None:
                return dest
        return source

    def get_source(self, destination: int) -> int:
        for mapping in self.mapping_ranges:
            dest = mapping.get_source(destination)
            if dest is not None:
                return dest
        return destination


class SeedRanges:
    def __init__(self, seeds: list[int]):
        self._seeds = seeds

    def __contains__(self, value: int) -> bool:
        seed_iterator = iter(self._seeds)
        while True:
            try:
                seed_start = next(seed_iterator)
                seed_range = next(seed_iterator)
                if value >= seed_start and value <= seed_start + seed_range - 1:
                    return True
            except StopIteration:
                return False


class Almanac:
    # assumption: Mappings come in order as needed => list
    def __init__(self, seeds: list[int]):
        self.seeds = seeds
        self.seed_ranges = SeedRanges(seeds)
        self._mappings: list[Mapping] = []

    def add(self, mapping: Mapping):
        self._mappings.append(mapping)

    def find_location(self, seed: int) -> int:
        src = seed
        for mapping in self._mappings:
            # assumpiton: last map is location
            src = mapping.get_destination(src)
        return src

    def find_seed(self, location: int) -> int:
        dest = location
        for mapping in self._mappings[::-1]:
            # assumpiton: last map is location
            dest = mapping.get_source(dest)
        return dest

    def find_seed_with_lowest_location(self) -> tuple[int, int]:
        location_to_seed = {self.find_location(seed): seed for seed in self.seeds}
        min_location = min(location_to_seed.keys())
        return min_location, location_to_seed[min_location]

    def find_seed_with_lowest_location_reverse(self):
        location = 0
        while True:
            seed = self.find_seed(location)
            if seed in self.seed_ranges:
                return location
            else:
                location += 1


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


file = "5/test_input.txt"
file = "5/input.txt"
almanac = parse(file)
lowest_location, seed = almanac.find_seed_with_lowest_location()
print(f"Part 1: Lowest location is {lowest_location} for initial seed {seed}")
print("Part 2: lowest location is:", almanac.find_seed_with_lowest_location_reverse())

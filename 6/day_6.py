from functools import reduce
from operator import mul


def get_number_of_ways_you_can_beat_the_record(
    total_time: int, record_distance: int
) -> int:
    return sum(
        [
            1
            for speed in range(0, total_time + 1)
            if (total_time - speed) * speed > record_distance
        ]
    )


# test input
times = (7, 15, 30)
distances = (9, 40, 200)

# 'real' input
times = (48, 93, 84, 66)
distances = (261, 1192, 1019, 1063)

numbers_of_ways_to_beat_the_record = [
    get_number_of_ways_you_can_beat_the_record(total_time, record_distance)
    for total_time, record_distance in zip(times, distances)
]
print("Part 1:", reduce(mul, numbers_of_ways_to_beat_the_record, 1))

# test input
time = 71530
record_distance = 940200

# 'real' input
time = 48938466
record_distance = 261119210191063

print("Part 2:", get_number_of_ways_you_can_beat_the_record(time, record_distance))

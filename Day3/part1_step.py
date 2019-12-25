import sys
import timeit

# Attempt #2
# The general idea is to get the set of points (relative to the central port) that each wire goes through.
# Then, get the intersection of the sets and iterate through that to find the closest point to the central port.
# With this attempt, I calculate the step through the endpoints to get the endpoints for each segment of the wire

def parse_wire_path(line):
    return line.replace('\n', '').split(',')

def parse_wire_paths(file_name):
    with open(file_name) as f:
        return [parse_wire_path(line) for line in f]

def get_next_wire_step(current_point, direction):
    magnitude = 1
    if direction == 'U':
        return (current_point[0], current_point[1] + magnitude)
    if direction == 'D':
        return (current_point[0], current_point[1] - magnitude)
    if direction == 'L':
        return (current_point[0] - magnitude, current_point[1])
    if direction == 'R':
        return (current_point[0] + magnitude, current_point[1])
    raise Exception

def get_wire_points(wire_path):
    current_point = (0, 0)
    wire_points = set()
    for wire_edge in wire_path:
        direction = wire_edge[0]
        magnitude = int(wire_edge[1:])
        for _ in range(magnitude):
            current_point = get_next_wire_step(current_point, direction)
            wire_points.add(current_point)
    return wire_points

def calculate_manhattan_distance(p, q):
    distance = 0
    for i in range(len(p)):
        distance += abs(p[i] - q[i])
    return distance

start = timeit.default_timer()
wire_paths = parse_wire_paths(sys.argv[1])
wire_points_for_each_wire = [get_wire_points(wire_path) for wire_path in wire_paths]
intersecting_points = set.intersection(*wire_points_for_each_wire)
intersecting_points_manhattan_distance_pair_list = [(point, calculate_manhattan_distance(point, (0, 0))) for point in intersecting_points]
intersecting_points_manhattan_distance_pair_list.sort(key=lambda p: p[1])
print(intersecting_points_manhattan_distance_pair_list)
end = timeit.default_timer()
print(f"Time: {end - start}")

import sys
import timeit

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

def calculate_step_distance(wire_path, point):
    current_point = (0, 0)
    step_distance = 0
    for wire_edge in wire_path:
        direction = wire_edge[0]
        magnitude = int(wire_edge[1:])
        for _ in range(magnitude):
            current_point = get_next_wire_step(current_point, direction)
            step_distance += 1
            if current_point == point:
                return step_distance
    raise Exception

start = timeit.default_timer()
wire_paths = parse_wire_paths(sys.argv[1])
wire_points_for_each_wire = [get_wire_points(wire_path) for wire_path in wire_paths]
intersecting_points = set.intersection(*wire_points_for_each_wire)
intersecting_points_step_distance_pair_list = [(point, sum([calculate_step_distance(wire_path, point) for wire_path in wire_paths])) for point in intersecting_points]
intersecting_points_step_distance_pair_list.sort(key=lambda p: p[1])
print(intersecting_points_step_distance_pair_list)
end = timeit.default_timer()
print(f"Time: {end - start}")

import sys
import timeit

# The general idea is to get the set of points (relative to the central port) that each wire goes through.
# Then, get the intersection of the sets and iterate through that to find the closest point to the central port.
# With this attempt, I calculate the endpoints for each wire line and use them to get each grid point

def parse_wire_path(line):
    return line.replace('\n', '').split(',')

def parse_wire_paths(file_name):
    with open(file_name) as f:
        return [parse_wire_path(line) for line in f]

def get_next_wire_turn_point(current_point, wire_edge):
    direction = wire_edge[0]
    magnitude = int(wire_edge[1:])
    if direction == 'U':
        return (current_point[0], current_point[1] + magnitude)
    if direction == 'D':
        return (current_point[0], current_point[1] - magnitude)
    if direction == 'L':
        return (current_point[0] - magnitude, current_point[1])
    if direction == 'R':
        return (current_point[0] + magnitude, current_point[1])
    raise Exception

# This function in isolation will do more than I really need for this approach
# It'll actually get a box of points between 2 points (excluding point1, including point2); but since this will be only used for edges, it'll really only be used for a line of points
# Probably won't use this for my next iteration of solving this problem anyways
def get_box_of_points_between_points(point1, point2):
    x_values = set(range(point1[0], point2[0]))
    x_values.discard(point1[0])
    x_values.add(point2[0])
    y_values = set(range(point1[1], point2[1]))
    y_values.discard(point1[1])
    y_values.add(point2[1])

    return {(x, y) for x in x_values for y in y_values}

def get_wire_points(wire_path):
    current_point = (0, 0)
    wire_points = set()
    for wire_edge in wire_path:
        next_point = get_next_wire_turn_point(current_point, wire_edge)
        wire_points = wire_points.union(get_box_of_points_between_points(current_point, next_point))
        current_point = next_point
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

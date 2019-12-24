import sys
import math

def calculate_module_fuel(mass):
    return math.floor(mass / 3) - 2

fuel_sum = 0
with open(sys.argv[1]) as f:
    for line in f:
        fuel_sum += calculate_module_fuel(int(line))

print(fuel_sum)

import sys
import math

def calculate_module_fuel(mass):
    fuel_for_mass = math.floor(mass / 3) - 2
    if (fuel_for_mass < 0):
        return 0
    return fuel_for_mass + calculate_module_fuel(fuel_for_mass)

fuel_sum = 0
with open(sys.argv[1]) as f:
    for line in f:
        fuel_sum += calculate_module_fuel(int(line))

print(fuel_sum)

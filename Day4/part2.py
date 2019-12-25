import sys

def non_decreasing_digits(num_str):
    for i in range(len(num_str) - 1):
        if int(num_str[i]) > int(num_str[i+1]):
            return False
    return True

num = 0
range_values = sys.argv[1]
range_start, range_end = map(int, range_values.split('-'))
for i in range(range_start, range_end + 1):
    str_i = str(i)
    if len(str_i) == 6 and non_decreasing_digits(str_i) and 2 in [str_i.count(digit) for digit in str_i]:
        num += 1
print(num)

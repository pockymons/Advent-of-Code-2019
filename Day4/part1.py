import sys

def has_consecutive_duplicate_characters(str):
    for i in range(len(str) - 1):
        if str[i] == str[i+1]:
            return True
    return False

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
    if len(str_i) == 6 and has_consecutive_duplicate_characters(str_i) and non_decreasing_digits(str_i):
        num += 1
print(num)

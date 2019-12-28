import sys
import intcode_computer

def convert_program_file_to_list(file_name):
    with open(file_name) as f:
        return list(map(int, f.read().split(',')))

raw_memory = convert_program_file_to_list(sys.argv[1])
computer = intcode_computer.IntcodeComputer(raw_memory)
computer.run_program()

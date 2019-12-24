import sys

def convert_program_file_to_list(file_name):
    with open(file_name) as f:
        return list(map(int, f.read().split(',')))

def restore_program_state(program_list):
    program_list[1] = 12
    program_list[2] = 2

def run_program(program_list):
    for i in range(0, len(program_list), 4):
        if program_list[i] == 1:
            program_list[program_list[i+3]] = program_list[program_list[i+1]] + program_list[program_list[i+2]]
        elif program_list[i] == 2:
            program_list[program_list[i+3]] = program_list[program_list[i+1]] * program_list[program_list[i+2]]
        elif program_list[i] == 99:
            return
        else:
            raise Exception

program_list = convert_program_file_to_list(sys.argv[1])
restore_program_state(program_list)
run_program(program_list)

print(program_list)

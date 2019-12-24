import sys

def convert_program_file_to_list(file_name):
    with open(file_name) as f:
        return list(map(int, f.read().split(',')))

def restore_program_state(program_list, noun, verb):
    program_list[1] = noun
    program_list[2] = verb

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

for i in range(0, 100):
    for j in range(0, 100):
        program_list = convert_program_file_to_list(sys.argv[1])
        restore_program_state(program_list, i, j)
        run_program(program_list)
        if program_list[0] == 19690720:
            print(f'Noun: {i}')
            print(f'Verb: {j}')

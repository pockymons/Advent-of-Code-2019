class IntcodeComputer:
    def __init__(self, raw_memory):
        self.memory = Memory(raw_memory)
        self.program = Program(self.memory) # only one program for now

    def run_program(self):
        self.program.run()

class Memory:
    def __init__(self, raw_memory):
        self.__memory = raw_memory

    def get(self, address):
        return self.__memory[address]

    def set(self, address, value):
        self.__memory[address] = value

    def get_address_range(self):
        return range(0, len(self.__memory))

class InstructionPointer:
    def __init__(self, address):
        self.__address = address

    def read(self):
        return self.__address

    def write(self, mode, value):
        if mode == "relative":
            self.__address += value
            return
        if mode == "absolute":
            self.__address = value
            return
        raise Exception(f"Invalid instruction pointer write mode: {mode}")

class Program:
    def __init__(self, memory, instruction_pointer_address=0):
        self.memory = memory
        self.instruction_pointer = InstructionPointer(instruction_pointer_address)
        self.__handler_by_opcode = {
            1: AddHandler(),
            2: MultiplicationHandler(),
            3: InputHandler(),
            4: OutputHandler(),
            5: JumpIfTrueHandler(),
            6: JumpIfFalseHandler(),
            7: LessThanHandler(),
            8: EqualsHandler(),
            99: HaltHandler()
        }

    def run(self):
        while self.instruction_pointer.read() in self.memory.get_address_range():
            # parse opcode and parameter modes
            # For now, parameters are represented as list of pairs where the first value is the parameter address and second value is the parameter mode
            parameter_modes_and_opcode = self.memory.get(self.instruction_pointer.read())
            opcode = parameter_modes_and_opcode % 100
            parameter_modes = parameter_modes_and_opcode // 100

            # get appropriate instruction handler
            handler = self.__handler_by_opcode[opcode]

            # bundle parameter adresses and parameter modes
            parameters = []
            for i in range(1, handler.number_of_parameters + 1):
                parameters.append((self.instruction_pointer.read() + i, parameter_modes % 10))
                parameter_modes //= 10

            # handle instruction
            instruction_handler_result = handler.handle(self.memory, parameters)
            if instruction_handler_result.result_code == 1:
                return

            # write to instruction pointer
            self.instruction_pointer.write(instruction_handler_result.instruction_pointer_write_mode, instruction_handler_result.instruction_pointer_write_value)

####### Instruction Handlers #######
def getParameterValue(memory, parameter_address, parameter_mode):
    parameter_value = memory.get(parameter_address)
    if parameter_mode == 0:
        return memory.get(parameter_value)
    if parameter_mode == 1:
        return parameter_value
    raise Exception(f"Invalid parameter mode: {parameter_mode}")

class InstructionHandlerResult:
    def __init__(self, result_code, instruction_pointer_write_mode, instruction_pointer_write_value):
        # 0: successful
        # 1: successful, halt program
        self.result_code = result_code 

        # "relative" - add the write value to the intruction pointer
        # "absolute" - set the instruction pointer value to the write value
        self.instruction_pointer_write_mode = instruction_pointer_write_mode

        self.instruction_pointer_write_value = instruction_pointer_write_value

class AddHandler:
    def __init__(self):
        self.number_of_parameters = 3

    def handle(self, memory, parameters):
        memory.set(memory.get(parameters[2][0]), getParameterValue(memory, parameters[0][0], parameters[0][1]) + getParameterValue(memory, parameters[1][0], parameters[1][1]))
        return InstructionHandlerResult(0, "relative", 4)

class MultiplicationHandler:
    def __init__(self):
        self.number_of_parameters = 3

    def handle(self, memory, parameters):
        memory.set(memory.get(parameters[2][0]), getParameterValue(memory, parameters[0][0], parameters[0][1]) * getParameterValue(memory, parameters[1][0], parameters[1][1]))
        return InstructionHandlerResult(0, "relative", 4)

class InputHandler:
    def __init__(self):
        self.number_of_parameters = 1

    def handle(self, memory, parameters):
        memory.set(memory.get(parameters[0][0]), int(input()))
        return InstructionHandlerResult(0, "relative", 2)

class OutputHandler:
    def __init__(self):
        self.number_of_parameters = 1

    def handle(self, memory, parameters):
        print(getParameterValue(memory, parameters[0][0], parameters[0][1]))
        return InstructionHandlerResult(0, "relative", 2)

class JumpIfTrueHandler:
    def __init__(self):
        self.number_of_parameters = 2

    def handle(self, memory, parameters):
        isTrue = getParameterValue(memory, parameters[0][0], parameters[0][1]) != 0
        if isTrue:
            absoluteAddress = getParameterValue(memory, parameters[1][0], parameters[1][1])
            return InstructionHandlerResult(0, "absolute", absoluteAddress)
        return InstructionHandlerResult(0, "relative", 3)

class JumpIfFalseHandler:
    def __init__(self):
        self.number_of_parameters = 2

    def handle(self, memory, parameters):
        isFalse = getParameterValue(memory, parameters[0][0], parameters[0][1]) == 0
        if isFalse:
            absoluteAddress = getParameterValue(memory, parameters[1][0], parameters[1][1])
            return InstructionHandlerResult(0, "absolute", absoluteAddress)
        return InstructionHandlerResult(0, "relative", 3)

class LessThanHandler:
    def __init__(self):
        self.number_of_parameters = 3

    def handle(self, memory, parameters):
        isLessThan = getParameterValue(memory, parameters[0][0], parameters[0][1]) < getParameterValue(memory, parameters[1][0], parameters[1][1])
        if isLessThan:
            lessThanValue = 1
        else:
            lessThanValue = 0
        memory.set(memory.get(parameters[2][0]), lessThanValue)
        return InstructionHandlerResult(0, "relative", 4)

class EqualsHandler:
    def __init__(self):
        self.number_of_parameters = 3

    def handle(self, memory, parameters):
        equals = getParameterValue(memory, parameters[0][0], parameters[0][1]) == getParameterValue(memory, parameters[1][0], parameters[1][1])
        if equals:
            equalsValue = 1
        else:
            equalsValue = 0
        memory.set(memory.get(parameters[2][0]), equalsValue)
        return InstructionHandlerResult(0, "relative", 4)

class HaltHandler:
    def __init__(self):
        self.number_of_parameters = 0

    def handle(self, memory, parameters):
        return InstructionHandlerResult(1, "relative", 0)

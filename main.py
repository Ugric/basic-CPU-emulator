import time


class CPU:
    def __init__(self, registers, memorysize, registersize) -> None:
        self.registers = [0] * registers
        self.pc = 0
        self.memory = [0] * memorysize
        self.maxsize = pow(2, registersize)

    def maxify(self, x):
        minus = -1 if x < 0 else 1
        return (abs(x) % self.maxsize) * minus

    def load(self, program):
        for i in range(len(program)):
            self.memory[i] = program[i]

    def run(self):
        while True:
            opcode = self.memory[self.pc]
            if opcode == 0:
                break
            self.execute(opcode)

    def execute(self, opcode):
        """Execute the given opcode"""
        if opcode == 1:
            self.add()
        elif opcode == 2:
            self.sub()
        elif opcode == 3:
            self.mul()
        elif opcode == 4:
            self.inp()
        elif opcode == 5:
            self.out()
        elif opcode == 6:
            self.jump_if_true()
        elif opcode == 7:
            self.jump_if_false()
        elif opcode == 8:
            self.regload()
        elif opcode == 9:
            self.memload()
        elif opcode == 10:
            self.regSet()
        elif opcode == 11:
            self.memSet()
        elif opcode == 12:
            self.snooze()
        else:
            raise Exception("Invalid opcode")

    def get_param_val(self, param, register):
        if register != False:
            self.registers[register] = self.memory[param+self.pc]
        else:
            return self.memory[param+self.pc]

    def write_memory(self, address, value):
        self.memory[address] = value

    def add(self):
        """Add"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        regDES = self.get_param_val(3, False)
        # Add the registers
        self.registers[regDES] = self.registers[regA] + self.registers[regB]
        # Increment the program counter
        self.pc += 4

    def sub(self):
        """Subtract"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        regDES = self.get_param_val(3, False)
        # Add the registers
        self.registers[regDES] = self.registers[regA] - self.registers[regB]
        # Increment the program counter
        self.pc += 4

    def mul(self):
        """Multiply"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(3, False)
        regDES = self.get_param_val(5, False)
        # Multiply the registers
        self.registers[regDES] = self.registers[regA] * self.registers[regB]
        # Increment the program counter
        self.pc += 4

    def inp(self):
        """Input"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        # Get the input
        inp = int(input("Input: "))
        # Write the input to the register
        self.registers[regA] = inp
        # Increment the program counter
        self.pc += 2

    def out(self):
        """Output"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        # Output the register
        if regA == 0:
            print(self.registers[regB], end='')
        else:
            print(chr(self.registers[regB]), end='')
        # Increment the program counter
        self.pc += 3

    def jump_if_true(self):
        """Jump if true"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        # Jump if the register is not 0
        if self.registers[regA] != 0:
            self.pc = regB
        else:
            self.pc += 3

    def jump_if_false(self):
        """Jump if true"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        # Jump if the register is not 0
        if self.registers[regA] == 0:
            self.pc = regB
        else:
            self.pc += 3

    def regload(self):
        """Load register"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        # Load the register
        self.registers[regA] = self.memory[regB]
        # Increment the program counter
        self.pc += 3

    def memload(self):
        """Load memory"""
        # Get the parameters and load them into the registers
        regA = self.get_param_val(1, False)
        regB = self.get_param_val(2, False)
        # Load the memory
        self.write_memory(regA, self.registers[regB])
        # Increment the program counter
        self.pc += 3

    def regSet(self):
        self.registers[self.get_param_val(
            1, False)] = self.get_param_val(2, False)
        self.pc += 3

    def memSet(self):
        self.write_memory(self.get_param_val(1, False),
                          self.get_param_val(2, False))
        self.pc += 3

    def snooze(self):
        time.sleep(self.registers[self.get_param_val(1, False)]/1000)
        self.pc += 2


CPU = CPU(8, 10000, 64)
file = open('machinecode.exe', 'r').read()
machinecode = []
for i in range(len(file)):
  machinecode.append(ord(file[i]))
CPU.load(machinecode)
CPU.run()

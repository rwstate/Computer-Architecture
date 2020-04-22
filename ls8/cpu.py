"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PSH = 0b01000101
POP = 0b01000110
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.r = [0] * 8
        self.r[7] = 0xF4
        self.pc = 0

    def ram_read(self, address):
        return self.r[address]
    
    def ram_write(self, address, value):
        self.r[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(sys.argv[1]) as f:
            for line in f:
              line = line.split('#')
              line = line[0].strip()
          
              if line == '':
                continue
          
              self.memory[address] = int(line, 2)
          
              address += 1



    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.r[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.memory[self.pc]
            operand_a = self.memory[self.pc + 1]
            operand_b = self.memory[self.pc + 2]
            if ir == HLT:
                break
            elif ir == LDI:
                self.r[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                print(self.r[operand_a])
                self.pc += 2
            elif ir == MUL:
                self.r[operand_a] = self.r[operand_a] * self.r[operand_b]
                self.pc += 3
            elif ir == PSH:
                # decrement the stack pointer
                self.r[SP] -= 1   # address_of_the_top_of_stack -= 1
            
                # copy value from register into memory
                reg_num = self.memory[self.pc + 1]
                value = self.r[reg_num]  # this is what we want to push
            
                address = self.r[SP]
                self.memory[address] = value   # store the value on the stack
                self.pc += 2
            elif ir == POP:
                reg_num = self.memory[self.pc + 1]
                address = self.r[SP]
                self.r[reg_num] = self.memory[address]
                self.r[SP] += 1
                self.pc += 2
            

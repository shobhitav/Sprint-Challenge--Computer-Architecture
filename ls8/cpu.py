"""CPU functionality."""

import sys

LDI=0b10000010
PRN=0b01000111
MUL=0b10100010 
HLT=0b00000001
PUSH=0b01000101  
POP=0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg=[0]*8
        self.PC=0
        self.IR=0
        # self.SP = self.reg[7]
        self.reg[7] = 0xF4
    
    def ram_read(self, address):
        return self.ram[address]
        
    def ram_write(self,value,address):
        self.ram[address] = value
    

    

    def load(self):
        """Load a program into memory."""

        address = 0
        
        program=[]
        
        if len(sys.argv) < 2:
            print("did you forget the file to open?")
            print('Usage: filename file_to_open')
            sys.exit()

        try:    
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split=line.split('#')
                    possible_num=comment_split[0]

                    if possible_num=='':
                        continue
                    if possible_num[0]=='1'or possible_num[0]=='0':
                        num=possible_num[:8]
                        # print(f'{num}:{int(num,2)}')

                        program.append(int(num,2))
        except:
            print(f'{sys.argv[0]}:{sys.argv[1]} not found')


        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def run(self):
        """Run the CPU."""
        SP=7  

        running = True

        while running:
            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
            # we want to know if it is alu command so want to find 3rd from left bit
            # (hence bit shifting and masking)
            # is_alu_command=(self.IR >>5) & 0b001 

            # if is_alu_command:
            #     self.alu(self.IR,operand_a,operand_b)
            #     self.PC+=3
            
            if self.IR == LDI :
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif self.IR == PRN :
                print(self.reg[operand_a]) 
                self.PC += 2
            
               
            # if self.IR == MUL:
            #     self.reg[operand_a] = self.reg[operand_a]*self.reg[operand_b]
            #     self.PC +=3

            elif self.IR == PUSH:
                self.reg[SP] -= 1
                # grab the current MA SP point to
                stack_address = self.reg[SP]
                # get a register number from the instruction
                register_num = self.ram_read(self.PC + 1)
                # get value out of the register
                value = self.reg[register_num]
                # werite the register value to a postition in the stack
                self.ram_write(stack_address, value)
                self.PC += 2
            
            elif self.IR == POP:
                # get the value from the memory
                stack_value = self.ram_read(self.reg[SP])
                # get the register number from instaruction in memory
                register_num = self.ram_read(self.PC + 1)
                # set the value of a register to the value held in the stack
                self.reg[register_num] = stack_value
                # increment SP
                self.reg[SP] += 1 
                self.PC += 2


            elif self.IR == HLT:
                running = False

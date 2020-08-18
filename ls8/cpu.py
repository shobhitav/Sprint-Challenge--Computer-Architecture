"""CPU functionality."""

import sys

LDI=0b10000010
PRN=0b01000111
MUL=0b10100010 
HLT=0b00000001
PUSH=0b01000101  
POP=0b01000110
CMP=0b10100111 
JMP=0b1010100 
JEQ=0b1010101
JNE=0b1010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg=[0]*8
        self.PC=0
        self.IR=0
        self.reg[7] = 0xF4
        self.flag = 0
    
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
            
            if self.IR == LDI :
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif self.IR == PRN :
                print(self.reg[operand_a]) 
                self.PC += 2
            
            elif self.IR == PUSH:

                self.reg[SP] -= 1
                # grab the current memory address SP point to
                stack_address = self.reg[SP]
                # get a register number from the instruction
                register_num = self.ram_read(self.PC + 1)
                # get value out of the register
                stack_value = self.reg[register_num]
                # werite the register value to a postition in the stack
                self.ram_write(stack_value, stack_address)
                self.PC += 2
            
            elif self.IR == POP:
                # get the value from the stack
                stack_value = self.ram_read(self.reg[SP])
                # get the register number from instruction in memory
                register_num = self.ram_read(self.PC + 1)
                # set the value of a register to the value held in the stack
                self.reg[register_num] = stack_value
                # increment SP
                self.reg[SP] += 1 
                self.PC += 2
                
                '''                
                `FL` bits: `00000LGE`   

                * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
                zero otherwise.
                * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
                registerB, zero otherwise.
                * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
                otherwise.
                '''

            
            elif self.IR == CMP:
                register_a = self.ram_read(self.PC + 1)
                register_b = self.ram_read(self.PC + 2)
                value_a = self.reg[register_a]
                value_b = self.reg[register_b]
                if value_a == value_b:
                    self.flag = 0b1
                elif value_a > value_b:
                    self.flag = 0b10
                elif value_b > value_a:
                    self.flag = 0b100
                self.PC += 3
            
                """
                Jump to the address stored in the given register.
                Set the PC to the address stored in the given register.
                """
            elif self.IR == JMP:
                register_a = self.ram_read(self.PC + 1)
                self.PC = self.reg[register_a]    

            # If equal flag is set (true), jump to the address stored in the given
            # register.
            elif self.IR == JEQ:
                if not self.flag & 0b1:
                    self.PC += 2
                elif self.flag & 0b1:
                    register_a = self.ram_read(self.PC + 1)
                    self.PC = self.reg[register_a]
            
            # If E flag is clear (false, 0), jump to the address stored in the given
            # register.
            elif self.IR == JNE:
                # masking with 0b1 
                if self.flag & 0b1:
                    self.PC+= 2
                elif not self.flag & 0b0:
                    register_a = self.ram_read(self.PC + 1)
                    self.PC = self.reg[register_a]

            
            
            elif self.IR == HLT:
                running = False

from . import InstructionSet

class ZInstructions(InstructionSet):
    '''Implements the basic Z-Code instructions'''
    def __init__(self):
        super(ZInstructions, self).__init__()


    def LIT(self, machine, *parameters):
        '''(LIT z)(m, d, b, h, o) = (m+1, z:d, b, h, o)'''
        machine.d.append(parameters[0])
        machine.m += 1

    def POP(self, machine, *parameters):
        '''(POP)(m, z:d, b, h, o) = (m+1, d, b, h, o)'''
        machine.d.pop()
        machine.m += 1

    def NOP(self, machine, *parameters):
        '''(NOP)(m, d, b, h, o) = (m+1, d, b, h, o)'''
        machine.m += 1

    def LOD(self, machine, *parameters):
        '''(LOD n)(m, d, b, h, o) = (m+1, h(n):d, b, h, o)'''
        addr = parameters[0]
        machine.d.append(machine.h[addr])
        machine.m += 1

    def STO(self, machine, *parameters):
        '''(STO n)(m, z:d, b, h, o) = (m+1, d, b, h[n/z], o)'''
        addr = parameters[0]
        machine.h[addr] = machine.d.pop()
        machine.m += 1

    def PRN(self, machine, *parameters):
        '''(PRN)(m, z:d, b, h, o) = (m+1, d, b, h, oz\n)'''
        machine.o += str(machine.d.pop()) + '\n'
        machine.m += 1

    def PRT(self, machine, *parameters):
        '''(PRT)(m, z:d, b, h, o) = (m+1, d, b, h, oz)'''
        machine.o += str(machine.d.pop())
        machine.m += 1

    def PRC(self, machine, *parameters):
        '''(PRT)(m, z:d, b, h, o) = (m+1, d, b, h, ochar(z))'''
        machine.o += chr(machine.d.pop())
        machine.m += 1

    def ADD(self, machine, *parameters):
        '''(ADD)(m, z1 z2:d, b, h, o) = (m+1, (z1+z2):d, b, h, o)'''
        machine.d.append(machine.d.pop() + machine.d.pop())
        machine.m += 1

    def SUB(self, machine, *parameters):
        '''(SUB)(m, z1 z2:d, b, h, o) = (m+1, (z2-z1):d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(machine.d.pop() - z2)
        machine.m += 1

    def MULT(self, machine, *parameters):
        '''(MULT)(m, z1 z2:d, b, h, o) = (m+1, (z1*z2):d, b, h, o)'''
        machine.d.append(int(machine.d.pop() * machine.d.pop()))
        machine.m += 1

    def DIV(self, machine, *parameters):
        '''(DIV)(m, z1 z2:d, b, h, o) = (m+1, (z2/z1):d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(machine.d.pop() // z2)
        machine.m += 1

    def JMP(self, machine, *parameters):
        '''(JMP n)(m, d, b, h, o) =
                if n > 0 then (n, d, b, h, o)
                if n < 0 then (stopaddr + n, d, b, h, o)
                if n = 0 then (stopaddr, d, b, h, o)'''
        if parameters[0] == 0:
            machine.m = len(machine.instructions) + 1
        elif parameters[0] < 0:
            machine.m = len(machine.instructions) + parameters[0] + 1
        else:
            machine.m = parameters[0]

    def JMC(self, machine, *parameters):
        '''(JMC n)(m, b:d, b, h, o) = 
                if b = 0 then
                    if n > 0 then (n, d, b, h, o)
                    if n < 0 then (stopaddr + n, d, b, h, o)
                    if n = 0 then (stopaddr, d, b, h, o)
                if b = 1 then (m+1, d, b, h, o)'''
        if parameters[0] == 0:
            target = len(machine.instructions) + 1
        elif parameters[0] < 0:
            target = len(machine.instructions) + parameters[0] + 1
        else:
            target = parameters[0]

        top = machine.d.pop()
        machine.m = target if top == 0 else machine.m + 1

    def EQ(self, machine, *parameters):
        '''(EQ)(m, z1 z2:d, b, h, o) =
                if z2 EQ z1 = true then (m+1, 1:d, b, h, o)
                if z2 EQ z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() == z2 else 0)
        machine.m += 1

    def NE(self, machine, *parameters):
        '''(NE)(m, z1 z2:d, b, h, o) =
                if z2 NE z1 = true then (m+1, 1:d, b, h, o)
                if z2 NE z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() != z2 else 0)
        machine.m += 1

    def LT(self, machine, *parameters):
        '''(LT)(m, z1 z2:d, b, h, o) =
                if z2 LT z1 = true then (m+1, 1:d, b, h, o)
                if z2 LT z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() < z2 else 0)
        machine.m += 1

    def GT(self, machine, *parameters):
        '''(GT)(m, z1 z2:d, b, h, o) =
                if z2 GT z1 = true then (m+1, 1:d, b, h, o)
                if z2 GT z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() > z2 else 0)
        machine.m += 1

    def LE(self, machine, *parameters):
        '''(LE)(m, z1 z2:d, b, h, o) =
                if z2 LE z1 = true then (m+1, 1:d, b, h, o)
                if z2 LE z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() <= z2 else 0)
        machine.m += 1

    def GE(self, machine, *parameters):
        '''(GE)(m, z1 z2:d, b, h, o) =
                if z2 GE z1 = true then (m+1, 1:d, b, h, o)
                if z2 GE z1 = false then (m+1, 0:d, b, h, o)'''
        z2 = machine.d.pop()
        machine.d.append(1 if machine.d.pop() >= z2 else 0)
        machine.m += 1

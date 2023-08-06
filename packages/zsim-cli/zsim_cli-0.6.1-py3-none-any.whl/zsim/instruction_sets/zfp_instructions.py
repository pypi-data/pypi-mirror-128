from . import ZInstructions

class ZFPInstructions(ZInstructions):
    '''Implements the basic Z-Code instructions'''
    def __init__(self):
        super(ZFPInstructions, self).__init__()


    def LODLOCAL(self, machine, *parameters):
        '''(LODLOCAL i)(m, d, b, h, o) = (m+1, b(b(1)-i+1):d, b, h, o)'''
        addr = parameters[0]
        blocksize = machine.b[-1]
        local = machine.b[-blocksize + addr - 1]

        machine.d.append(local)
        machine.m += 1

    def STOLOCAL(self, machine, *parameters):
        '''(STOLOCAL i)(m, z:d, b, h, o) = (m+1, d, b[(b(1)-i+1)/z], h, o)'''
        addr = parameters[0]
        blocksize = machine.b[-1]

        machine.b[-blocksize + addr - 1] = machine.d.pop()
        machine.m += 1

    def CALL(self, machine, *parameters):
        '''(CALL(ca, npar, lv1 ... lvn))(m, pnpar ... p1:d, b, h, o) =
                (ca, d, (npar+n+2) (m+1) lvn ... lv1 pnpar ... p1:b, h, o)'''
        target = parameters[0]
        parameterCount = parameters[1]
        localParameters = parameters[2]
        temp = []

        if parameterCount > 0:
            machine.b = machine.b + machine.d[-parameterCount:]
            del machine.d[-parameterCount:]

        for param in localParameters[::-1]:
            machine.b.append(param)

        machine.b.append(machine.m + 1)
        machine.b.append(parameterCount + len(localParameters) + 2)
        machine.m = target

    def RET(self, machine, *parameters):
        '''(RET)(m, d, (npar+n+2) ra lvn ... lv1 pnpar ... p1:b, h, o) =
                (ra, d, b, h, o)'''
        dl = machine.b.pop()
        ra = machine.b.pop()

        for i in range(dl - 2):
            machine.b.pop()

        machine.m = ra

    def HALT(self, machine, *parameters):
        '''(HALT)(m, d, b, h, o) = (stopaddr, d, b, h, o)'''
        machine.m = len(machine.instructions) + 1

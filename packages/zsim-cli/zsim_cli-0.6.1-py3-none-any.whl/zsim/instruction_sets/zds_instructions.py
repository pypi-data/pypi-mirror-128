from . import ZInstructions

class ZDSInstructions(ZInstructions):
    '''Implements the basic Z-Code instructions'''
    def __init__(self):
        super(ZDSInstructions, self).__init__()


    def LODI(self, machine, *parameters):
        '''(LODI)(m, a:d, b, h, o) = (m+1, h(a):d, b, h, o)'''
        a = machine.d.pop()
        machine.d.append(machine.h[a])
        machine.m += 1

    def STOI(self, machine, *parameters):
        '''(STOI)(m, z a:d, b, h, o) = (m+1, d, b, h[a/z], o)'''
        z = machine.d.pop()
        a = machine.d.pop()
        machine.h[a] = z
        machine.m += 1

    def AC(self, machine, *parameters):
        '''(AC n)(m, i:d, b, h, o) =
            if 0 <= i < n then (m+1, i:d, b, h, o)
            else throw Exception'''
        n = parameters[0]
        i = machine.d[0]

        if i < 0 or i >= n:
            raise Exception('Index out of bounds!')

        machine.m += 1

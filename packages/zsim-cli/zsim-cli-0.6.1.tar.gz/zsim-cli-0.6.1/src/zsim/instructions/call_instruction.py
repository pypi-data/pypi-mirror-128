from . import Instruction

class CallInstruction(Instruction):
    '''Represents a single CALL instruction'''
    def __init__(self, mnemonic, callback, *parameters):
        super(CallInstruction, self).__init__(mnemonic, callback, *parameters)

    def string(self, machine):
        target = self.parameters[0]

        for key, value in machine.jumps.items():
            if value == target:
                target = key
                break

        count = self.parameters[1]
        params = ' '.join(map(str, self.parameters[2]))

        return f'{ self.mnemonic }({ target }, { count }, { params })'

from . import Instruction

class JumpInstruction(Instruction):
    '''Represents a single JMP or JMC instruction'''
    def __init__(self, mnemonic, callback, *parameters):
        super(JumpInstruction, self).__init__(mnemonic, callback, *parameters)

    def string(self, machine):
        target = self.parameters[0]
        
        for key, value in machine.jumps.items():
            if value == target:
                target = key
                break

        return f'{ self.mnemonic } { target }'

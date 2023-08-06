class Instruction(object):
    '''Represents a single instruction'''
    def __init__(self, mnemonic, callback, *parameters):
        super(Instruction, self).__init__()
        self.mnemonic = mnemonic
        self.callback = callback
        self.parameters = parameters
    
    def __call__(self, machine):
        self.execute(machine)

    def execute(self, machine):
        self.callback(machine, *self.parameters)

    def string(self, machine):
        param_text = ' ' + ', '.join(map(str, self.parameters)) if len(self.parameters) > 0 else ''
        return f'{ self.mnemonic }{ param_text }'

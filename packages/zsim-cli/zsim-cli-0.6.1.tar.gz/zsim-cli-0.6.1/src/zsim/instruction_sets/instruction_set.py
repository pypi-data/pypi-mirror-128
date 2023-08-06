from abc import ABC, abstractmethod

class InstructionSet(ABC):
    '''Implements instructions as methods'''
    def __init__(self):
        super(InstructionSet, self).__init__()
    
    def __getitem__(self, instr: str):
        try:
            return getattr(self, instr)
        except Exception as e:
            raise NotImplementedError(f'Instruction { instr } is not part of this instruction set!')

    def __call__(self, instr, machine, *parameters):
        self[instr](machine, *parameters)

    def __dir__(self):
        return list(filter(lambda x: not x.startswith('_'), super(InstructionSet, self).__dir__()))
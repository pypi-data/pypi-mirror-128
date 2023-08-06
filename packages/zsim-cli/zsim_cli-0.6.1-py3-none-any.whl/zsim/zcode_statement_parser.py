from .parser import RecursiveDescent
from .instructions import Instruction, JumpInstruction, CallInstruction

class ZCodeStatementParser(RecursiveDescent):
    '''Validates if a given Z-Code'''
    def __init__(self, tokens, instruction_set, instruction_counter = 1, jump_targets = {}):
        super(ZCodeStatementParser, self).__init__(tokens)
        self.instruction_set = instruction_set
        self.instruction_counter = instruction_counter
        self.jump_targets = jump_targets
        self.instruction = None

    def program(self):
        self.__statement()

    def __statement(self):
        self.__labels()
        self.__command()

    def __labels(self):
        while self.accept('identifier'):
            self.jump_targets[self.previous.value] = self.instruction_counter
            self.expect('colon')
            self.accept_many('newline')
    
    def __command(self):
        if self.accept('command0'):
            self.instruction = Instruction(self.previous.value, self.instruction_set[self.previous.value])
            self.expect('semicolon')

        elif self.accept('command1'):
            self.instruction = Instruction(self.previous.value, self.instruction_set[self.previous.value])
            self.expect('number')
            self.instruction.parameters = (int(self.previous.value),)
            self.expect('semicolon')

        elif self.accept('jmpcommand'):
            self.instruction = JumpInstruction(self.previous.value, self.instruction_set[self.previous.value])
            self.expect('number', 'identifier')
            if self.previous.type == 'identifier':
                target = 0
                if self.previous.value in self.jump_targets:
                    target = self.jump_targets[self.previous.value]
            else:
                target = int(self.previous.value)
            self.instruction.parameters = (target,)
            self.expect('semicolon')

        elif self.accept('call'):
            self.instruction = CallInstruction(self.previous.value, self.instruction_set[self.previous.value])
            self.expect('openingParenthesis')
            self.expect('number', 'identifier')
            target = self.previous.value
            if self.previous.type == 'identifier':
                target = 0
                if self.previous.value in self.jump_targets:
                    target = self.jump_targets[self.previous.value]
            self.expect('comma')
            self.expect('number')
            param_count = int(self.previous.value)
            self.expect('comma')
            params = []
            while self.accept('number'):
                params.append(int(self.previous.value))
            self.instruction.parameters = (target, param_count, params)
            self.expect('closingParenthesis')
            self.expect('semicolon')
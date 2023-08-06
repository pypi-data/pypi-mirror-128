from .parser import Tokenizer, Token
from .instructions import Instruction, JumpInstruction, CallInstruction
from typing import List, Union, Optional
from copy import deepcopy

class Machine(object):
    '''Executes code based on an instruction set'''

    memory_scanner = tokenizer = (Tokenizer(eof=None)
            .token('open', r'\[')
            .token('close', r'\]')
            .token('number', r'0|-?[1-9][0-9]*')
            .token('assign', r'/')
            .token('comma', r',')
            .skip(r'\s+')
            .skip(r'\r')
            .skip(r'\n'))


    def __init__(self, instruction_set, tokens: List[Token], h:Optional[Union[str, dict]] = {}, format: Optional[str] = '({m}, {d}, {b}, {h}, {o})'):
        super(Machine, self).__init__()
        
        self.m = 1
        self.d = []
        self.b = []
        self.o = ''
        self.format = format
        self.jumps = {}
        self.instructions = []

        if isinstance(h, str):
            self.h = self.__parse_memory(h)
        elif isinstance(h, dict):
            self.h = h
        elif not h:
            self.h = {}
        else:
            raise Exception('Cannot parse memory allocation')

        if len(tokens) > 0:
            self.__parse_instructions(tokens, instruction_set)

        self.initial_h = deepcopy(self.h)



    def done(self):
        return self.m - 1 >= len(self.instructions)

    def step(self):
        instruction = self.get_next_instruction()
        if instruction:
            instruction(self)
        return deepcopy(self)

    def run(self, reset=True):
        if reset:
            self.reset()

        while not self.done():
            self.step()

    def enumerate_run(self, reset=True):
        if reset:
            self.reset()
            
        while not self.done():
            yield deepcopy(self)
            self.step()
        yield self

    def reset(self):
        self.m = 1
        self.d = []
        self.b = []
        self.o = ''
        self.h = deepcopy(self.initial_h)

    def get_next_instruction(self):
        if self.done():
            return

        return self.instructions[self.m - 1]

    def update_heap_pointer(self):
        return len(self.h) if 0 in self.h else len(self.h) + 1



    def __str__(self):
        dStr = ' '.join(map(str, self.d[::-1]))
        bStr = ' '.join(map(str, self.b[::-1]))
        hStr = '[' + ', '.join(map(lambda k: f'{ k[0] }/{ k[1] }', self.h.items())) + ']'
        return self.format.format(m=self.m, d=dStr, b=bStr, h=hStr, o=self.o.encode("unicode_escape").decode("utf-8"))

    def __getitem__(self, m: int) -> Instruction:
        if m > 0 and m <= len(self.instructions):
            return self.instructions[m - 1]



    def __parse_memory(self, memory: Optional[str]) -> dict:
        if not memory:
            return {}

        h = {}
        tokens = self.memory_scanner.tokenize(memory.strip())

        # Instead of doing another recursive descent we manually check the syntax here
        if tokens[0].type != 'open' or tokens[-1].type != 'close':
            raise Exception('Wrong syntax for memory allocation.')
        

        for i, token in enumerate(tokens):
            # New allocation starts after "[" or ","
            if token.type == 'open' or token.type == 'comma':
                # Check for <num>"/"<num>
                if (tokens[i+1].type == 'number' and
                        tokens[i+2].type == 'assign' and
                        tokens[i+3].type == 'number'):
                
                    addr = tokens[i+1].value
                    value = tokens[i+3].value
                    h[int(addr)] = int(value)
                else:
                    raise Exception('Wrong syntax for memory allocation.')

        return h

    def __parse_instructions(self, tokens, instruction_set) -> None:
        # Remove all newlines
        tokens = list(filter(lambda t: t.type != 'newline', tokens))
        instruction_counter = 1

        # Preprocess memory allocation in first line
        if (tokens[0].type == 'openingBracket' and
                tokens[1].type == 'number' and
                tokens[2].type == 'assignment' and
                tokens[3].type == 'number'):
            # Don't override explicitely set allocation
            if not int(tokens[1].value) in self.h:
                self.h[int(tokens[1].value)] = int(tokens[3].value)

            i = 4
            while (tokens[i].type == 'comma' and
                    tokens[i+1].type == 'number' and
                    tokens[i+2].type == 'assignment' and
                    tokens[i+3].type == 'number'):
                # Don't override explicitely set allocation
                if not int(tokens[i+1].value) in self.h:
                    self.h[int(tokens[i+1].value)] = int(tokens[i+3].value)
                i += 4

        # Preprocess all jump targets
        for i, token in enumerate(tokens):
            # Match for <identifier>":"
            if token.type == 'identifier' and tokens[i+1].type == 'colon':
                if token.value not in self.jumps:
                    self.jumps[token.value] = instruction_counter

            elif token.type == 'semicolon':
                instruction_counter += 1

        for i, token in enumerate(tokens):
            type = token.type
            value = token.value

            # Command in form <command>
            if type == 'command0':
                self.instructions.append(Instruction(value, instruction_set[value]))

            # Command in form <command> <parameter>
            elif type == 'command1':
                parameter = int(tokens[i+1].value)
                self.instructions.append(Instruction(value, instruction_set[value], parameter))

            # Command in form <jmpcommand> <identifier|number>
            elif type == 'jmpcommand':
                target_token = tokens[i + 1]
                target = 0

                if target_token.type == 'identifier' and target_token.value in self.jumps:
                    target = self.jumps[target_token.value]
                elif target_token.type == 'number':
                    target = int(target_token.value)

                self.instructions.append(JumpInstruction(value, instruction_set[value], target))

            # Command in form <call> "(" <identifier|number> "," <number> "," <number>* ")"
            elif type == 'call':
                target_token = tokens[i + 2]
                target = 0

                if target_token.type == 'identifier' and target_token.value in self.jumps:
                    target = self.jumps[target_token.value]
                elif target_token.type == 'number':
                    target = int(target_token.value)

                parameter_count = int(tokens[i + 4].value)
                parameter_index = i + 6
                parameters = []
                while tokens[parameter_index].type != 'closingParenthesis':
                    parameters.append(int(tokens[parameter_index].value))
                    parameter_index += 1

                self.instructions.append(CallInstruction(value, instruction_set[value], target, parameter_count, parameters))

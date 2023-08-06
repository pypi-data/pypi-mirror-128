from .token import Token
from .parse_exception import ParseException
from typing import List
from abc import ABC, abstractmethod
import inspect 

class RecursiveDescent(ABC):
    '''Implements the recursive descent pattern for parsing tokens.'''
    def __init__(self, tokens: List[Token]):
        super(RecursiveDescent, self).__init__()
        self.__tokens = tokens
        self.__index = 0
        self.last_error = None
    
    @property
    def token(self):
        if self.__index < 0 or self.__index >= len(self.__tokens):
            return
        return self.__tokens[self.__index]


    @property
    def previous(self):
        if self.__index > 0:
            return self.__tokens[self.__index - 1]

    @property
    def next(self):
        if self.__index + 1 < len(self.__tokens):
            return self.__tokens[self.__index + 1]

    @property
    def index(self):
        return self.__index


    def accept(self, *token_types, advance=True):
        if any([self.token and self.token.type == t for t in token_types]):
            if advance:
                self.advance()
            return True
        return False

    def expect(self, *token_types, advance=True):
        if not self.accept(*token_types, advance):
            self.error(*token_types)

    def error(self, *expected):
        caller = inspect.stack()[1].function
        if caller == 'expect':
            caller = inspect.stack()[2].function

        raise ParseException(list(expected), self.token, caller,
            previous=self.__tokens[:self.__index],
            next=self.__tokens[self.__index+1:-1])

    def accept_many(self, *token_types, amount=-1):
        found = 0
        while self.accept(*token_types) and found < amount:
            found += 1
        return found > 0

    def expect_many(self, *token_types, required=-1):
        found = 0
        while found < required:
            self.expect(*token_types)
            found += 1


    def advance(self):
        if self.next:
            self.__index += 1
        else:
            self.__index = -1

    def valid(self):
        self.__index = 0
        self.last_error = None
        
        try:
            self.program()
            return True
        except ParseException as ex:
            self.last_error = ex
            return False



    @abstractmethod
    def program(self):
        pass

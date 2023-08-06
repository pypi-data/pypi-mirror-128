from .parser import RecursiveDescent

class ZCodeParser(RecursiveDescent):
    '''Validates if a given Z-Code'''
    def __init__(self, tokens):
        super(ZCodeParser, self).__init__(tokens)

    def program(self):
        self.accept_many('newline')
        self.__memory()
        self.accept_many('newline')

        while self.token:
            self.__statement()
            self.accept_many('newline')
            self.accept('eof')

    def __memory(self):
        if self.accept('openingBracket'):
            self.__memory_assignment()
            self.expect('closingBracket')
            self.expect('newline')

    def __memory_assignment(self):
        if self.accept('number'):
            self.expect('assignment')
            self.expect('number')

        while self.accept('comma'):
            self.expect('number')
            self.expect('assignment')
            self.expect('number')

    def __statement(self):
        self.__labels()
        self.__command()

    def __labels(self):
        while self.accept('identifier'):
            self.expect('colon')
            self.accept_many('newline')
    
    def __command(self):
        if self.accept('command0'):
            self.expect('semicolon')

        elif self.accept('command1'):
            self.expect('number')
            self.expect('semicolon')

        elif self.accept('jmpcommand'):
            self.expect('number', 'identifier')
            self.expect('semicolon')

        elif self.accept('call'):
            self.expect('openingParenthesis')
            self.expect('number', 'identifier')
            self.expect('comma')
            self.expect('number')
            self.expect('comma')
            self.accept_many('number')
            self.expect('closingParenthesis')
            self.expect('semicolon')
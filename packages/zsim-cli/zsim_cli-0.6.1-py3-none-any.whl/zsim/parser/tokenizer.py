from .token_type import TokenType
from .token import Token
from typing import List, Optional
import re

class Tokenizer(object):
    '''Splits an input string into a list of tokens'''
    def __init__(self, default: str = 'unknown', skip: Optional[str] = 'skip', eof: Optional[str] = 'eof'):
        super(Tokenizer, self).__init__()
        self.default = default
        self.default_skip = skip
        self.eof = eof
        self.__types = []

    def token(self, token_type: str, *regex_list: List[str]):
        for regex in regex_list:
            self.__types.append(TokenType(token_type, regex, False))

        return self
    
    def skip(self, regex):
        self.__types.append(TokenType(self.default_skip, regex, True))
        return self


    def get_types(self) -> List[TokenType]:
        return self.__types


    def tokenize(self, text: str) -> List[Token]:
        if not text:
            return [ Token(self.default, None) ]

        # Start with one token which contains the entire text as its value
        tokens = [ Token(self.default, text) ]

        # Iterate all known types
        for token_type, regex, skip in self.__types:
            compiled_regex = re.compile(regex)
            if skip:
                tokens = list(filter(lambda t: t.type != self.default_skip, self.__extract_token_type(tokens, compiled_regex, self.default_skip)))
            else:
                tokens = list(self.__extract_token_type(tokens, compiled_regex, token_type))

        # Add a seperate EOF token if defined
        if self.eof:
            tokens.append(Token(self.eof, None))

        return tokens

    def __extract_token_type(self, tokens: List[Token], regex: re, token_type: str) -> Token:
        for token in tokens:
            # We only operate on non-default tokens, so yield the already processed ones
            if token.type != self.default:
                yield token
                continue

            # This token does not match, so we yield it unchanged
            if not regex.search(token.value):
                yield token
                continue

            index = 0
            for match in regex.finditer(token.value):
                # Yield everything before the match as a default token
                if index < match.start():
                    yield Token(self.default, token.value[index:match.start()])

                # Yield the new token with the match
                yield Token(token_type, match[0])
                index = match.end()

            # Yield everything after the match as a default token
            if index < len(token.value):
                yield Token(self.default, token.value[index:])

    def __str__(self) -> str:
        return f'Tokenizer types: {", ".join(map(lambda x: x.type, self.__types))}'

    def __repr__(self) -> str:
        '''Returns representation of the object'''
        properties = ('%s=%r' % (k, v) for k, v in self.__dict__.items() if not k.startswith('_'))
        return '%s(%s)' % (self.__class__.__name__, ', '.join(properties))

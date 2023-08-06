class ParseException(Exception):
    '''Exception raised for errors in the parser.'''
    def __init__(self, expected_list, actual, rule, previous=[], next=[]):
        previous_str = ''.join(map(lambda t: t.value, filter(lambda t: t, previous)))
        next_str = ''.join(map(lambda t: t.value, filter(lambda t: t, next)))

        message = f'Expected one of { expected_list }. '
        message += f'Got \'{ actual.type }\' instead in \'{ rule }\'! '
        message += f'({previous_str}>>>{actual.value}<<<{next_str})'

        super(ParseException, self).__init__(message)
        self.expected = expected_list
        self.actual = actual
        self.rule = rule
        
import click
import json as _json


def print_command_help(instruction_set, command):
    command_parts = command.split(' ')
    if len(command_parts) > 1:
        # help <command>
        matching = list(filter(lambda instr: instr.upper().startswith(command_parts[1].strip().upper()), dir(instruction_set)))
        if len(matching) > 0:
            # Found at least one entry
            for instruction in matching:
                click.echo(f'{instruction} - { instruction_set[instruction].__doc__ }')
        else:
            # Not found
            click.echo(f'\'{command_parts[1]}\' Does not seem to be part of this instruction set.')
    else:
        click.echo('Available commands:')
        for instruction in dir(instruction_set):
            click.echo(' ' + instruction)
        click.secho(' help - Show this help message.', fg='yellow')
        click.secho(' exit - Exit the interpreter.', fg='yellow')
        click.secho(' labels - Prints all defined labels.', fg='yellow')
        click.secho(' #noexec - Pushes a frame in which commands are not executed. Useful for function definition.', fg='yellow')
        click.secho(' #exec - Pops a previously defined \'#noexec\' frame.', fg='yellow')
        click.echo('Try \'help <command>\' for more information on a specific command.')


def interactive_mode(memory, instruction_set, format):
    from . import tokenizer, ZCodeStatementParser
    from .machine import Machine
    machine = Machine(instruction_set, [], memory, format)

    original = []
    tokens = []

    jump_targets = {}
    no_exec = 0 # Allows for contexts to be pushed before executed, like functions with labels, etc.

    click.secho('Welcome to the Z-Code interactive simulator! Try \'help\' for more information.', fg='yellow')
    while True:
        line = click.prompt(click.style('>' if no_exec == 0 else '#' * no_exec + '>', fg='yellow', bold=True), prompt_suffix=' ')

        # Special interactive mode commands
        if line.strip().lower().startswith('help'):
            print_command_help(instruction_set, line.strip().lower())
            continue
        elif line.strip().lower() == 'exit':
            click.echo(machine)
            break
        elif line.strip().lower() == 'labels':
            for label in jump_targets:
                click.echo(f'{label} -> {jump_targets[label]}')
            continue
        elif line.strip().lower() == '#noexec':
            no_exec += 1
            continue
        elif line.strip().lower() == '#exec':
            no_exec = max(0, no_exec - 1)
            continue

        # Parse and execute typed command
        original += [line]
        tokens += tokenizer.tokenize(line)

        if any([t.type == 'semicolon' for t in tokens]):
            parser = ZCodeStatementParser(tokens, instruction_set, machine.m, jump_targets)
            if not parser.valid():
                click.echo(f'{ click.style(parser.last_error, fg="red") }\nCannot execute command \'{ " ".join(original) }\'\n')
                continue

            original = []
            tokens = []

            machine.instructions.append(parser.instruction)

            if no_exec == 0:
                generator = machine.enumerate_run(reset=False)
                next(generator)
                for state in generator:
                    click.echo(machine)
            else:
                # To prevent continuing with the #noexec block we have to skip the just added instruction
                machine.m += 1


def read_file(file, encoding='utf_8', buffer_size=1024):
    if not file:
        return

    content = ''
    chunk = file.read(buffer_size)
    while chunk:
        content += chunk.decode(encoding)
        chunk = file.read(buffer_size)

    return content



@click.group()
def entry_point():
    pass



@click.command()
@click.option('--json/--no-json', default=False)
@click.option('-i', '--input', type=click.File('rb'))
@click.option('-it', '--interactive/--no-interactive', default=False, help='Run the simulator in an interactive interpreter mode.')
@click.option('-e','--encoding', type=str, default='utf_8', show_default=True, help='Encoding to use when using --input. Refer to "https://docs.python.org/3/library/codecs.html#standard-encodings" for possible values.') # click.Choice makes the help text a mess.
@click.option('-h', '--memory', type=str)
@click.option('--instructionset', type=click.Choice(['z', 'zfp', 'zds', 'zfpds'], case_sensitive=False), default='zfpds', show_default=True)
@click.option('--step/--no-step', default=False, help='Run step by step. Not compatible with --json')
@click.option('--full-output/--no-full-output', default=False, help='Show all states when simulating. Not compatible with --step')
@click.option('--format', default='({m}, {d}, {b}, {h}, {o})', show_default=True, type=str)
@click.argument('zcode', type=str, required=False)
@click.pass_context
def run(ctx, json, input, interactive, encoding, memory, instructionset, step, full_output, format, zcode):
    '''Run ZCODE'''

    from .instruction_sets import ZInstructions, ZFPInstructions, ZDSInstructions, ZFPDSInstructions
    instructionset_map = {
        'z': ZInstructions(),
        'zfp': ZFPInstructions(),
        'zds': ZDSInstructions(),
        'zfpds': ZFPDSInstructions(),
    }

    if interactive:
        interactive_mode(memory, instructionset_map[instructionset], format)
        return;

    if input:
        zcode = read_file(input, encoding)

    if not zcode:
        click.echo(ctx.get_help())
        return

    from . import tokenizer
    tokens = tokenizer.tokenize(zcode)

    from . import ZCodeParser
    parser = ZCodeParser(tokens)
    success = parser.valid()

    if not success:
        if json:
            output = { 'success': success, 'message': str(parser.last_error) }
            click.echo(_json.dumps(output))
        else:
            output = str(parser.last_error)
            click.echo(output)
        return


    from .machine import Machine
    machine = Machine(instructionset_map[instructionset], tokens, memory, format)


    if step:
        while not machine.done():
            next_instruction = machine.get_next_instruction()
            state_string = f'{machine}{" next: " + next_instruction.string(machine) if next_instruction else "" }'
            click.echo(state_string)
            click.pause()
            machine.step()
        click.echo(machine)
        return


    if json:
        states = [(state, machine[state.m]) for state in machine.enumerate_run()]
        output = {
            'success': True,
            'instruction_set': instructionset,
            'initial_memory': states[0][0].initial_h,
            'code': zcode,
            'final_state': {
                'm': machine.m,
                'd': machine.d,
                'b': machine.b,
                'h': machine.h,
                'o': machine.o,
            },
        }
        if full_output:
            output['states'] = [
                {
                    'state': {
                        'm': state_tuple[0].m,
                        'd': state_tuple[0].d,
                        'b': state_tuple[0].b,
                        'h': state_tuple[0].h,
                        'o': state_tuple[0].o,
                    },
                    'next_instruction': {
                        'command': state_tuple[1].string(machine),
                        'mnemonic': state_tuple[1].mnemonic,
                        'parameters': state_tuple[1].parameters,
                    } if state_tuple[1] else None
                } for state_tuple in states
            ]
        click.echo(_json.dumps(output))
    else:
        if full_output:
            for state_string in map(lambda x: f'{x}{" next: " + x[x.m].string(x) if machine[x.m] else "" }', machine.enumerate_run()):
                click.echo(state_string)
        else:
            machine.run()
            click.echo(machine)



@click.command()
@click.option('--json/--no-json', default=False)
@click.option('-i', '--input', type=click.File('rb'))
@click.option('--encoding', type=str, default='utf_8', show_default=True, help='Encoding to use when using --input. Refer to "https://docs.python.org/3/library/codecs.html#standard-encodings" for possible values.') # click.Choice makes the help text a mess.
@click.argument('zcode', type=str, required=False)
@click.pass_context
def validate(ctx, json, input, encoding, zcode):
    '''Validate ZCODE'''

    if input:
        zcode = read_file(input, encoding)

    if not zcode:
        click.echo(ctx.get_help())
        return

    from . import tokenizer
    tokens = tokenizer.tokenize(zcode)

    from . import ZCodeParser
    parser = ZCodeParser(tokens)
    success = parser.valid()

    if json:
        output = { 'success': success, 'message': 'Code is syntactically correct.' }
        if not success:
            output['message'] = str(parser.last_error)

        click.echo(_json.dumps(output))
    else:
        output = str(success)
        if not success:
            output = str(parser.last_error)

        click.echo(output)
        


@click.command()
@click.option('--json/--no-json', default=False)
@click.option('-i', '--input', type=click.File('rb'))
@click.option('--encoding', type=str, default='utf_8', show_default=True, help='Encoding to use when using --input. Refer to "https://docs.python.org/3/library/codecs.html#standard-encodings" for possible values.') # click.Choice makes the help text a mess.
@click.argument('zcode', type=str, required=False)
@click.pass_context
def tokenize(ctx, json, input, encoding, zcode):
    '''Tokenize ZCODE'''

    if input:
        zcode = read_file(input, encoding)

    if not zcode:
        click.echo(ctx.get_help())
        return

    from . import tokenizer
    tokens = tokenizer.tokenize(zcode)


    if json:
        output = _json.dumps(list(map(lambda x: {'type': x.type, 'value': x.value}, tokens)))
        click.echo(output)
    else:
        output = list(map(lambda x: (x.type, x.value), tokens))
        click.echo(output)



entry_point.add_command(run)
entry_point.add_command(validate)
entry_point.add_command(tokenize)

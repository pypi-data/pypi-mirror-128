<div id="top"></div>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://gitlab.com/justin_lehnen/zsim-cli">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">zsim-cli</h3>

  <p align="center">
    A simulator for an assembly like toy-language
    <br />
    <a href="https://gitlab.com/justin_lehnen/zsim-cli"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://gitlab.com/justin_lehnen/zsim-cli">View Demo</a>
    ·
    <a href="https://gitlab.com/justin_lehnen/zsim-cli/issues">Report Bug</a>
    ·
    <a href="https://gitlab.com/justin_lehnen/zsim-cli/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#tokenization">Tokenization</a></li>
        <li><a href="#validation">Validation</a></li>
        <li><a href="#simulating">Simulating</a></li>
        <li><a href="#using-interactive-mode">Using interactive mode</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![zsim-cli Demo][zsim-demo]](https://gitlab.com/justin_lehnen/zsim-cli)

Implemented for the compiler building course after the winter semester 2020 on the Aachen University of Applied Sciences.<br />
Z-Code is a simplified assembly like toy language created to prove that compiling to a temporary language like Java-Bytecode can be much easier than going from a high-level language directly to assembly.

Check out the syntax diagrams for detailed information on how the syntax of Z-Code is defined [here](ZCODE.md).

Sublime syntax highlighting for Z-Code available [here](zcode.sublime-syntax)!
[![Z-Code syntax highlighting][zcode-syntax-highlighting]](zcode.sublime-syntax)

It even works on [Termux](https://termux.com/)!

[![zsim on Termux][zsim-termux-screenshot]](https://termux.com/)

<div align="right">(<a href="#top">back to top</a>)</div>



### Built With

zsim-cli relies heavily on the following libraries.

* [Click](https://click.palletsprojects.com)
* [pytest](https://pytest.org)

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.6
  - Head over to _[https://python.org](https://www.python.org/downloads/)_ and install the binary suitable for your operation system. Make sure you can run it:
  ```sh
  python --version
  ```
* pip
  - Check if pip is already installed:
  ```sh
  pip --version
  ```
  - If your python installation does not come with pip pre-installed visit _[https://pip.pypa.io](https://pip.pypa.io/en/stable/installation/)_ to install it and then check again.

### Installation

1. Clone the repository
   ```sh
   git clone https://gitlab.com/justin_lehnen/zsim-cli.git
   cd zsim-cli
   ```

1. (Optionally) create a python virtual environment and enter it
   ```sh
   python -m venv venv
   # Windows
   venv/Scripts/activate.bat
   # Unix or MacOS
   source venv/bin/activate
   ```

1. Install using pip
   ```sh
   pip install -e .
   ```

1. Run unit tests
   ```sh
   pytest
   ```

And you're set!

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- USAGE EXAMPLES -->
## Usage

_For more examples, please refer to the [Documentation](https://gitlab.com/justin_lehnen/zsim-cli)_


### Tokenization
`zsim-cli tokenize [ZCODE]`
#### --json / --no-json
Type: `Boolean`
Default: `False`

If the flag is set, the output will be in JSON format.<br />
The JSON schema is `[ { "type": "<type>", "value": "<value>" }, ... ]`.

Examples:
```bash
# Tokenize code in JSON
zsim-cli tokenize "LIT 7; PRT;" --json
```
```bash
# Pipe output to a JSON parser like jq for powerful postprocessing!
zsim-cli tokenize "LIT 7; PRT;" --json | jq -r .[].type
```

#### -i, --input FILENAME
Type: `String`
Default: `None`

Set an input file to read the Z-Code from. `-` will use the stdin.
>If you're using Windows, remember that the default `cmd.exe` requires two EOF characters followed by return (see examples).

Examples:
```bash
# Tokenize file programs/test.zc
zsim-cli tokenize -i programs/test.zc
```
```bash
# Tokenize from stdin
zsim-cli tokenize -i -
LIT 7;
PRT;
# Windows
^Z <ENTER>
^Z <ENTER>
# Unix or MacOS
^D^D
```

#### --encoding TEXT
Type: `String`
Default: `"utf_8"`

Encoding to use when opening files with `-i, --input`.<br />
Refer to the [Python docs](https://docs.python.org/3/library/codecs.html#standard-encodings) for possible values.

Examples:
```bash
# Use ASCII encoding
zsim-cli tokenize -i ascii_encoded.zc --encoding ascii
```

### Validation
`zsim-cli validate [ZCODE]`
#### --json / --no-json
Type: `Boolean`
Default: `False`

If the flag is set, the output will be in JSON format.<br />
The JSON schema is `{ "success": <boolean>, "message": "<string>" }`.

Examples:
```bash
# Validate code in JSON
zsim-cli validate "LIT 7; PRT;" --json
```
```bash
# Pipe output to a JSON parser like jq for powerful postprocessing!
zsim-cli validate "LIT 7; PRT;" --json | jq -r .message
```

#### -i, --input FILENAME
Type: `String`
Default: `None`

Set an input file to read the Z-Code from. `-` will use the stdin.
>If you're using Windows, remember that the default `cmd.exe` requires two EOF characters followed by return (see examples).

Examples:
```bash
# Validate file programs/test.zc
zsim-cli validate -i programs/test.zc
```
```bash
# Validate from stdin
zsim-cli validate -i -
LIT 7;
PRT;
# Windows
^Z <ENTER>
^Z <ENTER>
# Unix or MacOS
^D^D
```

#### --encoding TEXT
Type: `String`
Default: `"utf_8"`

Encoding to use when opening files with `-i, --input`.<br />
Refer to the [Python docs](https://docs.python.org/3/library/codecs.html#standard-encodings) for possible values.

Examples:
```bash
# Use ASCII encoding
zsim-cli validate -i ascii_encoded.zc --encoding ascii
```

### Simulating
`zsim-cli run [ZCODE]`
#### --json / --no-json
Type: `Boolean`
Default: `False`

If the flag is set, the output will be in JSON format.<br />
This flag is **not compatible** with `--step`!<br />
The JSON schema is either `{ "success": <boolean>, "message": "<string>" }` for invalid zcode or <br />
```json
{
    "success": true,
    "instruction_set": "<z|zfp|zds|zfpds>",
    "initial_memory": { "..." },
    "code": "...",
    "final_state": {
        "m": 1,
        "d": [],
        "b": [],
        "h": {},
        "o": "",
    },
    "states": [
        {
            "state": { "Same as final_state" },
            "next_instruction": {
                "command": "...",
                "mnemonic": "...",
                "parameters": [ 1, 2, 3 ],
            },
        },
        "..."
    ],
}
```
when the execution was successful.

Examples:
```bash
# Run code and output information about the states in JSON
zsim-cli run "LIT 7; PRT;" --json
```
```bash
# Pipe output to a JSON parser like jq for powerful postprocessing!
zsim-cli run "LIT 7; PRT;" --json | jq -r .final_state.o
```

#### -i, --input FILENAME
Type: `String`
Default: `None`

Set an input file to read the Z-Code from. `-` will use the stdin.
>If you're using Windows, remember that the default `cmd.exe` requires two EOF characters followed by return (see examples).

Examples:
```bash
# Run file programs/test.zc
zsim-cli run -i programs/test.zc
```
```bash
# Run from stdin
zsim-cli run -i -
LIT 7;
PRT;
# Windows
^Z <ENTER>
^Z <ENTER>
# Unix or MacOS
^D^D
```

#### --encoding TEXT
Type: `String`
Default: `"utf_8"`

Encoding to use when opening files with `-i, --input`.<br />
Refer to the [Python docs](https://docs.python.org/3/library/codecs.html#standard-encodings) for possible values.

Examples:
```bash
# Use ASCII encoding
zsim-cli run -i ascii_encoded.zc --encoding ascii
```

#### -h, --memory TEXT
Type: `String`
Default: `"[]"`

Optionally overwrite the memory configuration for the executing code.<br />
The format is `[ <addr>/<value>, ... ]`.<br />
<!--Many -h or --memory can be used.-->

Examples:
```bash
# 10 + 5
zsim-cli run "LOD 1; LOD 2; ADD;" -h "[1/10, 2/5]"
```

#### --instructionset
Type: `String`
Default: `"zfpds"`

Set the instruction set. Each instruction set has different available instructions to use.<br />
For example `LODI` comes from `zds`, while `LODLOCAL` is defined in `zfp`.<br />
When you are unsure, stick with `zfpds` where all instructions are available.

Examples:
```bash
# Use a specific instruction-set
zsim-cli run "LIT 7; LIT 3; ADD;" --instructionset "z"
```

#### --step / --no-step
Type: `Boolean`
Default: `False`

If this flag is set, the execution will ask for confirmation after each step of the execution.<br />
This flag is **not compatible** with `--json` or `--full-output`!<br />

Examples:
```bash
# Go through Z-Code instruction by instruction
zsim-cli run "LIT 7; POP;" --step
```

#### --format
Type: `String`
Default: `"({m}, {d}, {b}, {h}, {o})"`

The `--format` option allows you to customize the regular output of the simulation.

Available placeholders:
 - `{m}` = instruction counter
 - `{d}` = data stack
 - `{b}` = procedure stack
 - `{h}` = heap memory
 - `{o}` = output

Examples:
```bash
# Use less components from the machine. This will yield "m: 5, h: [1/7], output: '7'"
zsim-cli run "LIT 7; STO 1; LOD 1; PRT;" --format "m: {m}, h: {h}, output: '{o}'"
```

#### --full-output / --no-full-output
Type: `Boolean`
Default: `False`

If this flag is given, all states are printed on the standard output.<br />
`--step` will ignore this option.

Examples:
```bash
# This will print all five states on the standard output
zsim-cli run "LIT 7; STO 1; LOD 1; PRT;" --full-output
```

#### -it, --interactive / --no-interactive
Type: `Boolean`
Default: `False`

Use this flag to start a Z-Code interpreter.<br />
Only `--format`, `--instructionset` and `-h, --memory` are compatible with this option.

Examples:
```bash
zsim-cli run -it
```

<div align="right">(<a href="#top">back to top</a>)</div>


### Using interactive mode

With `zsim-cli run -it` you can start an interactive interpreter to execute Z-Code line by line.

[![zsim-cli interactive mode Demo][zsim-interactive-demo]](https://gitlab.com/justin_lehnen/zsim-cli)

Using the interactive mode might present you with difficulties when using jumps or function calls.

The following code will **not** work in interactive mode:
```
LIT 6;
CALL(increment, 1,);
HALT;
increment: LODLOCAL 1;
LIT 1;
ADD;
RET;
```
`CALL(increment, 1,);` will fail since `increment` is not defined until later.<br />
To circumvent this issue two special commands have been added: `#noexec` and `#exec`.

These commands push and pop frames in which commands are not directly executed but parsed and saved.
The following example does the same as the Z-Code above, but uses `#noexec` and `#exec`:
```
> LIT 6;
> #noexec
#> f: LODLOCAL 1;
#> LIT 1;
#> ADD;
#> RET;
#> #exec
> CALL(f, 1,);
```
>Note the `#` in front of the prompt that tell how many `#noexec` frames are running.

You are not limited to defining functions that way either! The next example uses `#noexec` differently:
```
> #noexec          
#> add_and_sto: ADD;
#> STO 1;
#> HALT;     
#> #exec           
> LIT 4;           
> LIT 1;
> JMP add_and_sto;
> LOD 1;
> PRT;
```
In the standard simulation mode `HALT` would jump after `PRT` but since the last typed command was `JMP add_and_sto;` it will jump continue right after the instruction we just sent off!<br />

<div align="right">(<a href="#top">back to top</a>)</div>

<!-- ROADMAP -->
## Roadmap

- [x] Code execution
- [x] Memory allocation in code
- [x] Comments
- [x] Interactive mode
- [ ] Better -h, --memory parsing
- [ ] Error handling
- [ ] More instruction sets
- [ ] Documentation
- [ ] More sample programs


See the [open issues](https://gitlab.com/justin_lehnen/zsim-cli/issues) for a full list of proposed features (and known issues).

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a merge request. You can also simply open an issue with the label "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the project
1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
1. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
1. Use pytest to run unit tests (`pytest`)
1. Push to the branch (`git push origin feature/AmazingFeature`)
1. Open a merge request

### Codestyle

* Four space indentation
* One class per file
* Variables and functions are written in **snake_case**
* Class names are written in **PascalCase**

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- LICENSE -->
## License

Distributed under the Unlicense license. See [LICENSE][license-url] for more information.

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- CONTACT -->
## Contact

Justin Lehnen - justin.lehnen@alumni.fh-aachen.de - justin.lehnen@gmx.de

Project Link: [https://gitlab.com/justin_lehnen/zsim-cli](https://gitlab.com/justin_lehnen/zsim-cli)

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Aachen University of Applied Sciences](https://www.fh-aachen.de/en/)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)

<div align="right">(<a href="#top">back to top</a>)</div>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-url]: https://gitlab.com/justin_lehnen/zsim-cli/issues
[license-url]: https://gitlab.com/justin_lehnen/zsim-cli/blob/main/LICENSE
[zsim-screenshot]: images/screenshot.png
[zsim-demo]: images/demo.gif
[zsim-interactive-demo]: images/interactive.gif
[zsim-termux-screenshot]: images/termux.png
[zcode-syntax-highlighting]: images/syntax_highlighting.png

# agbpycc
<a href="https://gitmoji.dev">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji">
</a>

agbpycc is a python based compiler frontend for the [agbcc](https://github.com/pret/agbcc) compiler for the GameBoy Advance.
It provides an interface more similar to a modern gcc frontend, making it easier to use agbcc with other tools like compiler explorer.
agbpycc also does some processing of the assembly code, allowing for easier comparrison to other assembly.
This is due to its main usage in decompiling matching binaries.

## Installation
You can install agbpycc from pypi using pip.
This installs agbpycc as a command line tool, and also as an importable module.
You might want to use a virtual environment.
```shell script
pip install agbpycc
```

To install from source, you need to build the ASM Parser first.
This requires [antlr](https://www.antlr.org/).
The provided Makefile takes care of downloading the tool using wget.
Should wget not be available to you as a command, download the [antlr tool](https://www.antlr.org/download/antlr-4.9.2-complete.jar) manually, and place it in the projects directory.
```shell script
git clone https://gitlab.com/henny022/agbpycc
cd agbpycc
make install
```

To work with the project files directly, you need to install the required dependencies in addition to building the antlr files.
You can use the provided make target to do all this
```shell script
git clone https://gitlab.com/henny022/agbpycc
cd agbpycc
make setup
```

## Usage
To run agbpycc after install, use the `agbpycc` command line tool.
```shell script
agbpycc <arguments>
```
To run the files from source without installing run the python module from the project directory.
```shell script
python -m agbpycc <arguments>
```

The following is a list of the most basic arguments.
Run `agbpycc --help` to get a full list.
```
    --cc1   Path to the agbcc binary (required for compiling C)
    -o      output assembly file name
    -g      enable debug info
            processed output contains only file and line information
```
Assembling objects and Linking binaries are not yet supported.

### Examples
compile a file to cleaned assembly for nice human reading
```shell script
agbpycc --cc1 agbcc -g -o output.s input.c
```
clean assembly for nice human reading
```shell script
agbpycc -o output.s input.s
```

## Support
For problems with the tool, please use the [gitlab issue tracker](https://gitlab.com/henny022/agbpycc/-/issues).
For questions you can use the `tmc-misc` channel on the [zeldaret discord server](https://discord.zelda64.dev/).
Ping @Henny022 there.

## Contributing
To contribute your own code to this project, create a fork, do you changes and open a Merge Request.
Please use [gitmoji](https://gitmoji.dev/) in your commit messages, this creates a neat git history and allows to grasp the contents of a commit in a single look.

## Authors and acknowledgment
This was originally based on the `pycc.py` file in [this repo](https://github.com/SBird1337/cexplore), most of the has been modified or replaced since. ([original file](https://github.com/SBird1337/cexplore/blob/c8afb6bb4013d98e51487d6b2614f9d4ef9148cc/pycc.py))

Main Contributors:
- Octorock
- Henny022

## License
This is licensed under the Unlicense.
So you can use this code however you want.
Any credit you can give is very appreciated.

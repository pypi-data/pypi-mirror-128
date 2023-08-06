# jduargs

Simple command line argument parser.

## Installation
```bash
> pip(3) install (-U) jduargs
```

and

``` python
from jduargs import ArgumentParser
```
## Instanciation

```python
parser = ArgumentParser(description="default string", epilog="default string")
```
"description" and "epilog" are optional parameters. The provided strings will be respectively written at the beginning and at the end of the help provided -h or --help.

## Methods

```python
def add(self, key: str, short: str, type: type = str, required: bool = True, description: str = "", choices: list = [])
```
... to add an expected argument. The parameters are:
- key: the name of the parameter
- short: the short version of the key, as a single caracter
- type: the parameter type class
- required: define if the argument is mandatory or not. If set to False and the parameter is not provided, the default value is set by the type constructor
- description: explanation of what this parameter is used for. If no description is provided, an empty string is used instead
- choices: a list containing all possible values for this argument. If the passed value is not in the list, the program will stop with an error

```python
def from_json(self, path: str)
```
... to import the expected parameters from a json file. The dictionnary keys are the parameters name. For each key, it should contains the "short" and "type" keys as strings, and a required key as a boolean.
```python
def to_json(self, filename: str)
```
... to export the parameter dictionnary to a json file.

*Note: both methods exists in the "yaml" variant.*


```python
def compile(self, args: List[str]) -> dict
```
... to parse the provided argument list with respect to the defined parameters. It returns a dictionnary to access the different passed arguments values.

## Usage

First create an instance of the parser:

``` python
parser = ArgumentParser()
```

Then add the expected arguments to parse:

``` python
parser.add("file", "f", description="file name without extension", choices = ["file1","file2"])
parser.add("path", "p", required=False, description="path to database tree")
```

Compile the parser with the input arguments provided from command line:

``` python
arguments = parser.compile(sys.argv[1:])
```
arguments is a dictionnary containing all parsed values. THe key is the name of the parameter given to the add() method.


You can also access each parameters with the simple bracket operator, directly on the parser, after compiling it:

``` python
file = parser["file"]
path = parser["path"]
```

## Full example

### Main python code: 
```python
import sys
from jduargs.parser import ArgumentParser

parser = ArgumentParser(
    description="Example use of the argument parser.",
    epilog="Have fun !",
)

parser.add("file", "f", description="file name w/o extension", choices=["file1","file2"])
parser.add("path", "p", required=False, description="path to main folder")

results = parser.compile(sys.argv[1:])

file = results["file"] // similar to parser["file"]
path = results["path"] // similar to parser["path"]

print(f"{file=}")
print(f"{path=}")
```

### Script execution:
```bash
$ python main.py
To get help, use -h or --help command line options.
```

```bash
$ python main.py -h
usage: .\test.py -ffile [-ppath]

Example use of the argument parser.

positional arguments:
-f: file           <class 'str'>
        file name w/o extension
        Possible values are ['file1', 'file2'].

optional arguments:
-p: path           <class 'str'>
        path to main folder
-h, --help
        show this help message and exit        

Have fun !
```

```bash
$ python .\test.py -ffile3 
Provided file not in ['file1', 'file2']
```

```bash
$ python .\test.py -ffile2
file='file2'
path=''
```

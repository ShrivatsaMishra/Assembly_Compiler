# Two Pass Assembler

This python file takes an input in Assembly Language and then converts it to it's corresponding  Machine Language code, storing it in output.txt

## Installation

__No installation is required__ once the file is extracted.

## Usage

The Assembler first asks if you would like to provide the input file or would like to use the default input file i.e. __Input.txt.__

The output is automatically stored in __output.txt__, however if errors are present then the errors are written in the output file as well as being displayed on the monitor.

To add comments simply put a __#__ symbol before it and all the text after it would be ignored by the Assembler. This Assembler __does not allow__ multi line comments. However you __can__ have a line with just comments.

The symbols and variable __have to be declared after the END statement.__ However if any other statement is present after the END statement the assembler will display an error.

After the First Pass the program displays the __Machine Opcode Table__, the __Label Table__, the __Literal Table__, the __Symbol Table__ as well as the __Data Table__.

At the end of the Second Pass the program print the __Output/ Errors__ in the __output file__ and also prints both of them in the Monitor.

If there are any errors in the assembly code then those are written in the Output.txt file. If not then the correct assembly code is written.

## Example

The __input.txt__ file already has a machine code in it which is :

```
START
INP X
INP Y
CLA
LOOP: LAC A #This is a Label
ADD Y
BRN LOOP
DSP X
END
DS X # This declares a symbol
DC ONE 1 # This declares a constant with value 1
DS Y
DC TEN 10
```
This code gives an __output__ :

```
1000 01100000
1000 01101000
0000
0001 01100000
0011 01101000
0110 00100100
1001 01100000
```

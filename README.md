# HLint

A simple interpreter for **HL**, a small hypothetical programming language, written for the CSS125P (Principles of Programming Languages) course project.

The interpreter is a single Python file, `HLInt.py`, with no dependencies outside the standard library.

## What it does

Given an HL source file, `HLInt.py`:

1. Removes all spaces, tabs, and line breaks, and writes the result to `NOSPACES.TXT`.
2. Writes every reserved word and symbol found in the program to `RES_SYM.TXT`.
3. Checks the program and prints `ERROR` (with the line number and reason) or `NO ERROR(S) FOUND`.
4. If there are no errors, executes the program and prints its output.

## Quick start

Requires Python 3.8 or later.

```bash
git clone https://github.com/Kaigosama/HLint.git
cd HLint
python HLInt.py programs/PROG3.HL
```

Output:

```
HLInt - HL Interpreter
Source file : programs/PROG3.HL
Created     : NOSPACES.TXT, RES_SYM.TXT

NO ERROR(S) FOUND

Program output:
3
```

Run `python HLInt.py` with no argument to be prompted for a file name.

## The HL language

```
x: integer;
y: double;
x:= 3;
y:= 1.25;
if(x<5)
  output<<x+y;
```

| Construct | Syntax | Example |
|---|---|---|
| Declaration | `<name> : <type> ;` | `x: integer;` `y: double;` |
| Assignment | `<name> := <expr> ;` (`=` also accepted) | `x:= 5;` `y = 4 + 2.56;` |
| Expression | values or variables joined by `+` / `-` | `x + y - 1` |
| Output | `output << "<string>" ;` or `output << <expr> ;` | `output<<"hello";` `output<<x;` |
| One-way if | `if ( <expr> <relop> <expr> ) <statement>` | `if(x<5) output<<x;` |

**Data types**

- `integer`: whole numbers. Integer values written in the program must be a single digit (0–9).
- `double`: real numbers with up to 2 decimal places. Results print with 2 decimals.

**Relational operators:** `>`, `<`, `==`, `!=`

**Rules**

- Variables must be declared before use and cannot be declared twice.
- A double value cannot be stored in an integer variable. An integer stored in a double variable is converted.
- Keywords and variable names are case-insensitive (`If`, `OUTPUT`, and `X` are valid).
- Strings may use straight (`"`) or curly (`“ ”`) quotes.

## Output files

For `PROG3.HL`:

`NOSPACES.TXT`
```
x:integer;y:double;x:=3;if(x<5)output<<x;
```

`RES_SYM.TXT` (unique entries, in order of first appearance)
```
RESERVED WORDS:
integer
double
if
output
SYMBOLS:
:
;
:=
(
<
)
<<
```

## Error reporting

```
$ python HLInt.py programs/ERROR1.HL
...
ERROR
  line 2: expected ';', found 'output'
```

Detected errors include:

- missing or unexpected symbols
- invalid characters, such as `*`
- undeclared or redeclared variables
- a double value assigned to an integer variable
- multi-digit integer values or doubles with more than 2 decimals
- a variable used before it has a value (reported at run time)

## Project files

```
HLint/
├── HLInt.py            interpreter: tokenizer, recursive-descent parser, executor
├── test_hlint.py       self-check for samples, output files, and error cases
├── programs/
│   ├── PROG1.HL        sample programs from the project specification
│   ├── PROG2.HL
│   ├── PROG3.HL
│   ├── ERROR1.HL       missing ';'
│   ├── ERROR2.HL       undeclared variable
│   └── ERROR3.HL       unsupported '*'
└── docs/
    ├── CSS125P_Project_Documentation_HLint.docx
    ├── MEMBERS.txt     group members
    └── SUBMISSION.md   submission checklist
```

`NOSPACES.TXT` and `RES_SYM.TXT` are created in the folder you run the interpreter from.

## Testing

```bash
python test_hlint.py
```

Prints `All tests passed.` on success.

## Expected results

| Program | Output |
|---|---|
| `PROG1.HL` | `5` |
| `PROG2.HL` | `4.25` |
| `PROG3.HL` | `3` |
| `ERROR1.HL` | `ERROR` – line 2: expected `;` |
| `ERROR2.HL` | `ERROR` – line 2: variable `y` is not declared |
| `ERROR3.HL` | `ERROR` – line 2: invalid character `*` |

## Team

**Group 3**, section AM2

- Guiang, Tristan Kier
- Adame, Samuela Ysebelle
- Sebastian, Kendrick

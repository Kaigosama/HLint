# HLint

A small interpreter for **HL**, a minimal toy programming language with integers, doubles, arithmetic, output, and one-way `if` statements.

HLint is a single Python file, `HLInt.py`, with no dependencies outside the standard library.

## Features

For each HL source file, HLint:

1. Strips all whitespace and writes the result to `NOSPACES.TXT`.
2. Lists every reserved word and symbol in the program in `RES_SYM.TXT`.
3. Checks syntax and types, and prints `ERROR` (with the line number and reason) or `NO ERROR(S) FOUND`.
4. If the program is valid, executes it and prints its output.

## Quick start

Requires Python 3.8 or later.

```bash
git clone https://github.com/Kaigosama/HLint.git
cd HLint
python HLInt.py programs/PROG3.HL
```

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

### Data types

- `integer`: whole numbers. Integer literals are single digits (0–9).
- `double`: real numbers with up to 2 decimal places. Results print with 2 decimals.

### Relational operators

`>`, `<`, `==`, `!=`

### Rules

- Variables must be declared before use and cannot be declared twice.
- A double value cannot be stored in an integer variable. An integer stored in a double variable is converted.
- Keywords and variable names are case-insensitive (`If`, `OUTPUT`, and `X` are valid).
- Strings may use straight (`"`) or curly (`“ ”`) quotes.

## How it works

`HLInt.py` runs the source through three stages:

| Stage | Function | Job |
|---|---|---|
| Tokenizer | `tokenize()` | Splits the source into keywords, identifiers, numbers, strings, and symbols with one regular expression |
| Parser | `Parser` | Recursive-descent parser that builds a list of statements and checks declarations and types |
| Executor | `run()` | Walks the statements, evaluates expressions, and prints output |

All errors are raised as `HLError` with the line number.

## Output files

For `programs/PROG3.HL`:

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

Both files are written to the folder you run HLint from.

## Error reporting

```
$ python HLInt.py programs/ERROR1.HL
...
ERROR
  line 2: expected ';', found 'output'
```

Detected errors:

- missing or unexpected symbols
- invalid characters, such as `*`
- undeclared or redeclared variables
- a double value assigned to an integer variable
- multi-digit integer literals or doubles with more than 2 decimals
- a variable used before it has a value (reported at run time)

## Examples

| Program | Result |
|---|---|
| `programs/PROG1.HL` | `5` |
| `programs/PROG2.HL` | `4.25` |
| `programs/PROG3.HL` | `3` |
| `programs/ERROR1.HL` | `ERROR` – line 2: expected `;` |
| `programs/ERROR2.HL` | `ERROR` – line 2: variable `y` is not declared |
| `programs/ERROR3.HL` | `ERROR` – line 2: invalid character `*` |

## Project structure

```
HLint/
├── HLInt.py        interpreter
├── test_hlint.py   tests
├── programs/       example HL programs
└── docs/           documentation
```

## Testing

```bash
python test_hlint.py
```

Prints `All tests passed.` on success.

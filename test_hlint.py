"""Self-check for HLInt.py. Run: python test_hlint.py"""
import os

from HLInt import HLError, parse, reserved_and_symbols, run, strip_spaces, tokenize


def interpret(source):
    lines = []
    run(parse(tokenize(source)), out=lines.append)
    return lines


def read(name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "programs", name)
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def fails(source, expected):
    try:
        interpret(source)
    except HLError as e:
        assert expected in str(e), f"{expected!r} not in {str(e)!r}"
        return
    raise AssertionError(f"no error for: {source!r}")


# Spec sample programs
assert interpret(read("PROG1.HL")) == ["5"]
assert interpret(read("PROG2.HL")) == ["4.25"]
assert interpret(read("PROG3.HL")) == ["3"]

# NOSPACES.TXT / RES_SYM.TXT content
assert strip_spaces(read("PROG1.HL")) == "x:integer;x:=5;output<<x;"
assert reserved_and_symbols(tokenize(read("PROG3.HL"))) == (
    ["integer", "double", "if", "output"], [":", ";", ":=", "(", "<", ")", "<<"])

# Spec examples: curly quotes, case-insensitive keywords, false if, '=' assignment
assert interpret('output<<”hello world”;') == ["hello world"]
assert interpret('x:integer; x:=6; If(x<5) Output<<X; output<<"done";') == ["done"]
assert interpret('x:integer; y:double; x = 3 + 2; y = 4 + 2.56; output<<x; output<<y;') == ["5", "6.56"]
assert interpret('y:double; y:=2; output<<y-0.75;') == ["1.25"]
assert interpret('x:integer; x:=4; if(x!=5) if(x>3) output<<x-9;') == ["-5"]

# Error programs
fails(read("ERROR1.HL"), "line 2: expected ';'")
fails(read("ERROR2.HL"), "variable 'y' is not declared")
fails(read("ERROR3.HL"), "invalid character '*'")
fails("x:integer; x:=2.5;", "cannot assign a double")
fails("x:integer; x:=10;", "single digit")
fails("y:double; y:=1.255;", "2 decimal places")
fails("x:integer; x:integer;", "already declared")
fails("x:integer; if(x=5) output<<x;", "relational operator")
fails("x:integer; output<<x;", "before it has a value")
fails("x:integer; if(x<5)", "expected a statement")
fails("x:string;", "expected data type")

print("All tests passed.")

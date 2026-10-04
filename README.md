# HLint

`HLInt.py` is a simple interpreter for **HL**, the hypothetical language from the CSS125P project specification.

For each HL source file, the interpreter:

1. Removes all whitespace and writes the result to `NOSPACES.TXT`.
2. Writes the reserved words and symbols it finds to `RES_SYM.TXT`.
3. Prints `ERROR` (with the line number and reason) or `NO ERROR(S) FOUND`.
4. If there are no errors, runs the program and prints its output.

It needs Python 3.8 or later and uses only the standard library.

## Usage

```
python HLInt.py PROG2.HL
```

```
HLInt - HL Interpreter
Source file : PROG2.HL
Created     : NOSPACES.TXT, RES_SYM.TXT

NO ERROR(S) FOUND

Program output:
4.25
```

Run without an argument to be prompted for the file name.

## The HL language

| Construct | Example |
|---|---|
| Declaration | `x: integer;` `y: double;` |
| Assignment | `x := 5;` or `x = 3 + 2;` |
| Arithmetic | `+` and `-` on single-digit integers and doubles with up to 2 decimals |
| Output | `output << "hello";` `output << x + y;` |
| One-way if | `if (x < 5) output << x;` with `>`, `<`, `==`, `!=` |

Keywords and variable names are case-insensitive.

## Files

| File | Purpose |
|---|---|
| `HLInt.py` | The interpreter |
| `PROG1.HL` – `PROG3.HL` | Sample programs from the specification |
| `ERROR1.HL` – `ERROR3.HL` | Programs with errors (missing `;`, undeclared variable, unsupported `*`) |
| `test_hlint.py` | Self-check: `python test_hlint.py` |
| `docs/` | Project documentation (CSS125P template) |
| `MEMBERS.txt` | Group members |

## Submission checklist

- [ ] Fill in the group name and members in `docs/CSS125P_Project_Documentation_HLint.docx` and `MEMBERS.txt`.
- [ ] Take screenshots of `PROG1.HL`, `PROG2.HL`, `PROG3.HL`, `ERROR1.HL`, and the output files. Paste them into Section III of the documentation, replacing the yellow placeholders.
- [ ] Export the documentation to PDF (in Word: File > Save As > PDF).
- [ ] Zip the program files: `HLInt.py`, `*.HL`, `test_hlint.py`, and `README.md`.
- [ ] Zip the screenshots.
- [ ] Record the video demo. The first frame must show the complete names of all members.
- [ ] Upload the program zip, screenshot zip, video, and `MEMBERS.txt` to Google Drive. Submit the link and the PDF. Only one member submits.

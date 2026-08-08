SWE4201 FINAL ASSIGNMENT - AI-ASSISTED CODE DOCUMENTATION
============================================================

Student: Carelofy (Reg. No. CST/22/SWE/00823)
Course: SWE4201
Submitted to: Prof. B. S. Galadanci

------------------------------------------------------------
PROGRAM DESCRIPTION
------------------------------------------------------------
The program is a Library Management System written in Python.
It is a single-file, in-memory application (no external database)
that models a small library's day-to-day operations.

Core features:
  1. Add books to a catalogue (supports multiple copies per title)
  2. Register library members
  3. Borrow a book (with a 14-day loan period)
  4. Return a book (automatically calculates a late fine of 0.5
     currency units per day overdue)
  5. Pay down a member's outstanding fine balance
  6. Search the catalogue by title or by author (case-insensitive
     substring match)
  7. List all currently overdue loans across all members
  8. Export the full current state (catalogue + membership data)
     to a JSON file

The file also includes a demo() function that walks through a
sample scenario: adding books, registering members, borrowing,
returning a book late to demonstrate fine calculation, searching,
and exporting the final state to library_state.json.

------------------------------------------------------------
FILES SUBMITTED
------------------------------------------------------------
1. original_program.py
   - The original program with NO comments or docstrings, as
     required by the assignment.

2. commented_program.py
   - The same program, unchanged in behaviour, with comments
     and docstrings added by an AI assistant (Claude) to explain
     what each class, method, and non-obvious line does.

3. README.TXT
   - This file.

------------------------------------------------------------
HOW THE AI DOCUMENTATION WAS PRODUCED
------------------------------------------------------------
The uncommented program (original_program.py) was given to an
AI assistant (Claude, by Anthropic) with a request to analyse the
code and add appropriate comments and docstrings without altering
the program's logic or behaviour. The AI:
  - Added a module-level docstring summarising the program's
    purpose and features.
  - Added class-level docstrings explaining the responsibility
    of each class (Book, Member, Library).
  - Added method-level docstrings explaining parameters,
    return values, and side effects (e.g. what borrow_book()
    checks before allowing a loan, how return_book() calculates
    fines).
  - Added inline comments next to non-obvious lines (e.g. the
    fines threshold check in borrow_book(), the ISO-date
    conversion in Member.to_dict()).

No functional code was changed during this process; only
comments and docstrings were inserted. This was verified by
comparing original_program.py and commented_program.py line by
line for logic differences.

------------------------------------------------------------
HOW TO RUN
------------------------------------------------------------
Requires Python 3. No external dependencies.

    python3 original_program.py
    python3 commented_program.py

Both will run the demo() function and produce identical output,
including a library_state.json file in the working directory.

# Task 7: Custom Language Interpreter

A custom interpreter built from scratch in **Python** to tokenize, parse, and execute a simple programming language featuring variables, arithmetic, and control flow.

---

## Features

- **Lexical Analysis (Lexer)**
  - Tokenizes raw source code into meaningful units.
  - Supports keywords (`while`), identifiers, numbers, and operators.

- **Abstract Syntax Tree (AST)**
  - Represents the structure of the code hierarchically.
  - Includes nodes for assignments, binary operations, and loops.

- **Recursive Descent Parsing**
  - Converts tokens into an AST based on language grammar.
  - Handles operator precedence and block structures.

- **Dynamic Interpretation**
  - Evaluates the AST recursively.
  - Maintains a runtime environment (variable scope) for data storage.

- **Control Flow**
  - Implements `while` loops for iterative execution.
  - Supports conditional expressions.

---

## Tech Stack

- **Python 3**

---

## Project Workflow

1. **Tokenization**: The `lexer` scans the input string and produces a list of tokens.
2. **Parsing**: The `parser` processes tokens to build an Abstract Syntax Tree (AST).
3. **Evaluation**: The `interpreter` traverses the AST and executes each node.
4. **Environment Management**: Variables are stored and updated in a dictionary-based environment.

---

## Language Logic

- **Variables**: Assign values using the `=` operator (e.g., `x = 5`).
- **Arithmetic**: Supports basic operations like addition (`+`) and comparisons (`<`).
- **Loops**: `while` loops execute blocks of code as long as a condition is met.

---

## Installation

```bash
python main.py
```

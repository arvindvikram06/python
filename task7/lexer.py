import re

# Defined patterns for language tokens
TOKEN_SPEC = [
    ("EQ", r'=='),
    ("NE", r'!='),
    ("LE", r'<='),
    ("GE", r'>='),
    ("LT", r'<'),
    ("GT", r'>'),
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("MUL", r'\*'),
    ("DIV", r'/'),
    ("EQUAL", r'='),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("LBRACE", r'\{'),
    ("RBRACE", r'\}'),
    ("WS", r'\s+'),
]

KEYWORDS = {"if", "else", "while"}

# Converts source code string into a list of tokens
def tokenize(code):
    tokens = []

    while code:
        for name, pattern in TOKEN_SPEC:
            match = re.match(pattern, code)
            if match:
                text = match.group(0)
                code = code[len(text):]

                # Skip whitespace
                if name == "WS":
                    break

                # Identify keywords
                if name == "IDENT" and text in KEYWORDS:
                    name = text.upper()

                tokens.append((name, text))
                break
        else:
            raise Exception(f"Invalid token at: {code[:10]}...")

    tokens.append(("EOF", ""))
    return tokens
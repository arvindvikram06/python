import re

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

KEYWORDS = {"if", "else","while"}

def tokenize(code):
    tokens = []

    while code:
        for name, pattern in TOKEN_SPEC:
            match = re.match(pattern, code)
            if match:
                text = match.group(0)
                code = code[len(text):]

                if name == "WS":
                    break

                if name == "IDENT" and text in KEYWORDS:
                    name = text.upper()

                tokens.append((name, text))
                break
        else:
            raise Exception(f"Invalid token: {code}")

    tokens.append(("EOF", ""))
    return tokens

    
print(tokenize("a = 3 * 7"))
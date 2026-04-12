import re

TOKEN_SPEC = [
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_][a-zA-Z0-9_]*'),

    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("MUL", r'\*'),
    ("DIV", r'/'),

    ("EQUAL", r'='),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),

    ("WS", r'\s+'),
]

def tokenize(code):
    tokens = []

    while code:
        for name, pattern in TOKEN_SPEC:
            match = re.match(pattern, code)

            if match:
                text = match.group(0)
                code = code[len(text):]
                if name != "WS":
                    # print("not whitespace",name)
                    tokens.append((name, text))
                # else:
                    # print("whitespace",name)
                break
        else:
            raise Exception(f"Invalid token: {code}")

    tokens.append(("EOF", ""))
    return tokens

    
print(tokenize("a = 3 * 7"))
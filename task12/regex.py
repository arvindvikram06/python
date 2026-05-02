import re

text = "(p:Person)"
print(re.findall(r'\((.*?)\)', text))
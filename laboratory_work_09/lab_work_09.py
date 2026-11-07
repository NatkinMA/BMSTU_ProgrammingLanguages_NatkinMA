import re

text = "Today is 23.10.2026 and we are teaching the regular expression. 14:58 14.58"

print(re.findall(r"\b(0[1-9]|[12]\d|3[01])[./-](0[1-9]|1[0-2])[./-](\d{4})\b",
                 text))

print(re.findall(r"\b(?:[01]?[0-9]|2[0-3]):[0-5][0-9]\b",
                 text))


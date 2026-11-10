import re

s =  '''```json
{
    "tool": "temperature",
    "inputdatavalue": "new york"
}
```'''

h =  '''```json{"tool": "temperature","inputdatavalue": "new york"}```'''

if not s.split()[0] == "{" or not s.split()[-1] == "}":
    match = re.search(r"\{.*\}", s, re.DOTALL)
    if match:
        s = match.group()

print(s)
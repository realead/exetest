#echo input to stdout and twice to stderr
from __future__ import print_function
import sys

input_content=sys.stdin.read()

if not input_content:
    exit(42)

print(input_content)
print(input_content*2, file=sys.stderr)
exit(0)

#echo input to stdout and twice to stderr

import sys

input_content=sys.stdin.read()

if not input_content:
    exit(42)

print input_content
print >> sys.stderr, input_content*2
exit(0)

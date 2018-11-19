from __future__ import print_function
import sys

if len(sys.argv) == 1:
    exit(42)

print(sys.argv[1])
print(sys.argv[1]+sys.argv[1], file=sys.stderr)
exit(0)

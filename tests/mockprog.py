import sys

if len(sys.argv) == 1:
    exit(42)

print sys.argv[1]
print >> sys.stderr, sys.argv[1]+sys.argv[1]
exit(0)

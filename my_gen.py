from docopt import docopt
import sys
import collections
from random import shuffle

help = """
Usage:
  my_gen.py <Number>

"""
arguments = docopt(help)

if arguments['<Number>'].isdigit() == False:
    print(help)
    sys.exit(0)

N = int(arguments['<Number>'])

if N < 3:
    print("N-puzzle must be superior or egal 3")
    sys.exit(0)

sequence = [i for i in range(N * N)]
shuffle(sequence)

print('#My own generator')
print(str(N))

for i in range(1, len(sequence)):
    if i % N == 0:
        print(sequence[i])
    else:
        print(sequence[i], end=" ")
print(sequence[0])

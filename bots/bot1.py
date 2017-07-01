from __future__ import print_function
import sys
import random

BETTOR = int(sys.argv[1])
VALUE = int(sys.argv[2])

if VALUE > 19:
    print(0)
elif VALUE > 15:
    print(random.getrandbits(1))
else:
    print(1)





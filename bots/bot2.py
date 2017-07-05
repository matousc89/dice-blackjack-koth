from __future__ import print_function
from sys import argv

# drop name of the script
argv = argv[1:] 
    

TASK = argv[0]
VALUE = int(argv[1])
MY_LOG = argv[2]
OP_LOG = argv[3]
if TASK == "PLACE":   
    MY_COUNT = int(argv[4])
    OP_COUNT = int(argv[5])
    # decide how much bet as bettor  
    print(min(5,max(1, 5-21-VALUE)))           
if TASK == "ANSWER":
    MY_COUNT = int(argv[4])
    OP_COUNT = int(argv[5])
    OP_BET = int(argv[6])
    # decide whether to accept the bet or not
    acceptable = min(5,max(1, 5-21-VALUE))
    print(1 if acceptable >= OP_BET else 0) 
elif TASK == "ROLL":
    ROLE = argv[4]   
    # decide whether to roll or not     
    if VALUE >= 18:
        print(0)
    else:
        print(1)





'''
multiline comment
in python
'''

# from dictionary import * #here * is like import everything from dictionary but this will also import the global variable from dictionary and we can somehow mutate the global variable which is not a good design
import time
from sys import argv #to access command line
from dictionary import check,load,unload,size
import re

DICTIONARY = "dictionary/large.txt" #constant
LENGTH = 45

if len(argv) !=2 and len(argv)!=3:
    exit("Usage: speller [dictionary] text")

(time_load, time_check, time_size, time_unload) = (0.0,0.0,0.0,0.0) #tuple unpacking

dictionary = argv[1] if len(argv) == 3 else DICTIONARY

before = time.process_time()
loaded = load(dictionary)
after = time.process_time()

if not loaded:
    exit(f"Could not load {dictionary}.")

time_load = after - before

#text = argv[2] if len(argv) == 3 else argv[1]
text = argv[-1]
file = open(text,"r",encoding="latin_1")
if not file:
    print(f"Could not open {text}.")
    unload()
    exit(1)

print("MISSPELLED WORDS")

index,misspelling, words = 0,0,0
word = ""

while True:
    c = file.read(1)
    if not c:
        break
    if re.match(r"[A-Za-z]",c) or (c=="'" and index > 0):
        word += c
        index +=1

        if index > LENGTH:
            while True:
                c = file.read(1)
                if not c or not re.match(r"[A-Za-z]",c):
                    break
            index,word = 0,""
    elif c.isdigit():
        while True:
            c = file.read(1)
            if not c or (not c.isalpha() and not c.isdigit()):
                break
            index,word = 0,""
    elif index > 0:
        words += 1
        before = time.process_time()
        misspelled = not check(word)
        after = time.process_time()

        time_check+= after - before

        if(misspelled):
            #print(word)
            misspelling+=1
        index , word = 0 , ""
file.close()

before = time.process_time()
n = size()
after = time.process_time()

time_size = after - before

before = time.process_time()
unloaded = unload()
after = time.process_time()

if not unloaded:
    print(f"Could not load {dictionary}.")
    exit(1)

time_unload = after - before

print(f"\n WORDS MISSPELLED: {misspelling}")
print(f"\n WORDS IN DICTIONARY: {n}")
print(f"\n WORDS IN TEXT: {words}")
print(f"\n TIME IN LOAD: {time_load:.2f}")
print(f"\n TIME IN CHECK: {time_check:.2f}")
print(f"\n TIME IN SIZE: {time_size:.2f}")
print(f"\n TIME IN UNLOAD: {time_unload:.2f}")
print(f"\n TOTAL TIME: {time_load + time_check:.2f}")

#SUCCESS
exit(0)

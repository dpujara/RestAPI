words = set()

def check(word):
    return word.lower() in words

def load(dictionary):
    with open(dictionary,"r") as file:
        for line in file:
            words.add(line.rstrip("\n"))
    return True

def size():
    return len(words)

def unload():
    return True

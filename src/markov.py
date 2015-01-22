import random
import sys
from collections import defaultdict
from bisect import bisect
from time import time

THRESHOLD = 2
WINDOW_SIZE = 1
SENTENCES = 3
LENGTH = 100
NUM_EXAMPLES = 20

num_words = 0

# Returns a "clean" list of words present in this file
# Removes strange characters and numbers (relatively infrequent)
def get_data(filename):
    f = open(filename)
    words = [w.lower().strip('(){}[]#",1234567890') for w in f.read().split()\
             if ":" not in w]
    f.close()
    return words

transitions = defaultdict(lambda: defaultdict(lambda:0))

# Initialize the transitions dicitonary
def markov_init(filename = "quotes_1mil.txt"):
    data = get_data(filename)
    print "Done Parsing File"
    for i, d in enumerate(data[:-WINDOW_SIZE]):
        d_key = d
        if WINDOW_SIZE > 1:
            d_key = tuple(data[i:i+WINDOW_SIZE])
        transitions[d_key][data[i+WINDOW_SIZE]] += 1
    for k, v in transitions.iteritems():
        counts = sum(v.values())
        last = 0.0
        keys = v.keys()
        # Convert probabilities to cumulative probabilities
        for i in range(len(keys)):
            last += v[keys[i]]/float(counts)
            if i == len(keys) - 1:
                v[keys[i]] = 1
            else:
                v[keys[i]] = last

def generate_example(start=None, sentences = SENTENCES, length = LENGTH):
    if start == None:
        start = random.choice([k for k, v in transitions.iteritems()\
                               if len(v) >= THRESHOLD])
    sentence = ""

    next_word = start
    num_sentences = 0
    words = 0
    for _ in range(length):
        if num_sentences >= sentences:
            break
        if WINDOW_SIZE == 1:
            sentence += " " + next_word
        else:
            sentence += " " + next_word[0]
        words += 1
        if sentence[-1] in (".", "!", "?"):
            num_sentences +=1
        possible_words = sorted(transitions[next_word].items(), \
                                key=lambda x:x[1])
        if len(possible_words) == 0:
            sentence += "."
            num_sentences += 1
            next_word = random.choice([k for k, v in transitions.iteritems()\
                                       if len(v) >= THRESHOLD])
            continue
        next_word_index = bisect([p[1] for p in possible_words],\
                                 random.random())
        if WINDOW_SIZE == 1:
            next_word = possible_words[next_word_index][0]
        else:
            next_word = tuple([next_word[1], \
                              possible_words[next_word_index][0]])
    global num_words
    num_words += words
    return sentence[1:]

def main(argv):
    filename = None
    if len(argv) > 1:
        print("Usage: python markov.py filename")
        return
    elif len(argv) == 1:
        filename = argv[0]

    if filename:
        t = time()
        markov_init(filename)
    else:
        t = time()
        markov_init()

    s = time()
    print ("Initializing the Markov matrix took: "+str(s-t)+" seconds.")

    t = time()
    for _ in range(NUM_EXAMPLES):
        print(generate_example()+"\n\n")
    s = time()
    print("Generating "+str(NUM_EXAMPLES)+" examples took on average: "+\
          str((s-t)/NUM_EXAMPLES)+" seconds per example.")

    print("Average sentence length: "+\
          str(float(num_words)/(NUM_EXAMPLES*SENTENCES))+" words")

if __name__ == "__main__":
   main(sys.argv[1:])

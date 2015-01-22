The program can be run as: 
python markov.py filename
or
python markov.py

The second case defaults to opening the file "quotes_1mil.txt"

The data sets can be downloaded from:
MASC: http://www.anc.org/data/masc/downloads/data-download/
Download the (500k) - data only and unpack.
One sample dataset (tweets1.txt) is included with this project

IMDB: ftp://ftp.fu-berlin.de/pub/misc/movies/database/
Download quotes.lst.gz and unpack
If quotes.lst is downloaded and unpacked, then the script firstmil.sh
should output the first million lines of dialogue into "quotes_1mil.txt"

There are 5 parameters that are at the top of the program and can be
tinkered with. The parameter THRESHOLD is used to determine which
states to prune for our initial choice of state. The parameter
WINDOW_SIZE determines the order of the Markov chain/the length of the
sliding window. The parameter SENTENCES determines how many sentences
to generate per example. The parameter LENGTH is the maximum length of
a single example (to prevent extremely long chains). The parameter
NUM_EXAMPLES is the number of examples to generate.

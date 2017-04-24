#!/usr/bin/env python


import word2vec, sys, codecs
from trec_car.read_data import *


def makeInputFile(cbor, output):

    outputFile = codecs.open(output, 'w', 'utf-8')

    with open(cbor, 'rb') as corpus:
        for p in iter_paragraphs(corpus):
            outputFile.write( p.get_text())
    outputFile.close()



def build( input_text ):

    word2vec.word2phrase(input_text, input_text + ".phrase", verbose=True)
    word2vec.word2vec(input_text + ".phrase", input_text + ".bin", size=100, verbose=True)





if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Args: <passages file> <output file>")
        exit()
    makeInputFile(sys.argv[1], sys.argv[2])
    build(sys.argv[2])

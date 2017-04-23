#!/usr/bin/env python

INDEX_DIR = "BaseIndexFolder"
# INDEX_DIR = "IndexFiles.index"
import sys, os, lucene
import codecs
import re
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher


"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        print ()
        print ("Hit enter with no input to quit.")
        command = raw_input("Query:")
        if command == '':
            return

        print()
        print ("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print ("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            # print ('id:', doc.get("paraId"), 'Contents', doc.get("contents"))
            print ('id:', doc.get("paraId"))


def run1(searcher, analyzer, queries, hits_per_query, output_file):
    #queries = [ [query_text],[query_id]]
    queries_text = queries[0]
    queries_ids = queries[1]

    if len(queries_text)!= len(queries_ids):
        print("Query errors")
        exit()
    for i in range(len(queries_text)):
        query_as_text = queries_text[i]

        query_as_id = queries_ids[i]
        query = QueryParser("contents", analyzer).parse(query_as_text)
        scoreDocs = searcher.search(query, hits_per_query).scoreDocs
        print ("%s total matching documents." % len(scoreDocs))

        rank=1
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            # print ('id:', doc.get("paraId"), 'Contents', doc.get("contents"))
            print ('id:', doc.get("paraId"))
            search_result_query = ' '.join([query_as_id,str(0),
                                            doc.get("paraId"),
                                            str(rank),
                                            str(1.0/rank),
                                            "BBT"])
            # print(search_result_query)
            output_file.write(search_result_query+"\n")
            rank += 1


def search_engine_1(queries, hits):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run1(searcher, analyzer, queries, hits, run_file)
    del searcher
    run_file.close()


def search_engine_general():
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run1(searcher, analyzer)
    del searcher
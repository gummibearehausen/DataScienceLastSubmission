#!/usr/bin/env python
# -*- coding: utf-8 -*-

INDEX_DIR = "BaseIndexFolder"
# INDEX_DIR = "IndexFiles.index"
import sys, os, lucene
import codecs, sys
import re
from Parsing import tag_annotator
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, ScoreDoc

import word2vec


from Indexer_1 import IndexFiles



def content_from_id(id):
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(INDEX_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()

    query = QueryParser("paraId", analyzer).parse(id)
    scoreDocs = searcher.search(query, 1).scoreDocs
    if len(scoreDocs) == 1:
        return searcher.doc(scoreDocs[0].doc).get("contents")
    else:
        return None



def run(searcher, analyzer):
    while True:
        print ()
        print ("Hit enter with no input to quit.")
        command = input("Query:")
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


def text_normalisation(scoreDoc, doc_facet, searcher):
    lucene_doc = searcher.doc(scoreDoc.doc)
    para_text = lucene_doc.get(doc_facet)
    # print(para_text)
    normalised_text = re.sub("[^A-Za-z0-9]", " ", para_text)
    return normalised_text


def top_k_pseudo_feedback(scoreDocs, top_k, doc_facet, searcher):
    pseudo_fk = [text_normalisation(s, doc_facet, searcher) for s in scoreDocs[:top_k]]
    return pseudo_fk


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
        print("Query " + str(i) + " " + query_as_text)
        runfile_writer(scoreDocs, searcher, output_file, query_as_id)


def run2(searcher, analyzer, queries, hits_per_query, output_file, k, facet):
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


        top_k = int(k)
        pseudo_feedback = top_k_pseudo_feedback(scoreDocs, top_k, facet, searcher)
        pseudo_feedback_as_text = " ".join(pseudo_feedback)
        query_prime = QueryParser("contents", analyzer).parse(query_as_text+pseudo_feedback_as_text)

        scoreDocs_prime = searcher.search(query_prime, hits_per_query).scoreDocs

        runfile_writer(scoreDocs_prime, searcher, output_file, query_as_id)


def run5(searcher, analyzer, queries, hits_per_query, output_file, k):
    from tools import Annotator
    annotator = Annotator()
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

        top_k = int(k)
        pseudo_feedback = top_k_pseudo_feedback(scoreDocs, top_k, "contents", searcher)

        def srlannotation(article_from_pseudo_result):
            try:
                srl_anno=annotator.getAnnotations(article_from_pseudo_result)
                return srl_anno
            except:
                return None
        args_top_k_pseudo = [ tag_annotator(srlannotation(ps),"srl")
                              for ps in pseudo_feedback]
        args_as_text = ""
        if len(args_top_k_pseudo)==1:
            args_as_text = args_top_k_pseudo[0]

        elif len(args_top_k_pseudo)>1:
            args_as_text = " ".join(args_top_k_pseudo)
        new_query_as_text = query_as_text+" "+re.sub(r'[^A-Za-z0-9]', ' ', args_as_text)
        query_prime = QueryParser("contents", analyzer).parse(new_query_as_text)

        scoreDocs_prime = searcher.search(query_prime, hits_per_query).scoreDocs
        runfile_writer(scoreDocs_prime, searcher, output_file, query_as_id)


def run3(searcher, analyzer, queries, hits_per_query, output_file):
    queries_text = queries[0]
    queries_ids = queries[1]
    page_names = queries[2]

    if len(queries_text)!= len(queries_ids):
        print("Query errors")
        exit()
    last_title = None
    for i in range(len(queries_text)):
        query_as_text = queries_text[i]
        query_as_id = queries_ids[i]
        page_name = page_names[i]
        current_title = page_name

        print(query_as_text)

        if last_title != current_title:
            query = QueryParser("contents", analyzer).parse(page_name)
            scoreDocs = searcher.search(query, hits_per_query).scoreDocs
            IndexFiles([ searcher.doc(d.doc) for d in scoreDocs ], "./tempindex", reindex=True)
            last_title = current_title

        directory2 = SimpleFSDirectory(Paths.get("./tempindex"))
        searcher2 = IndexSearcher(DirectoryReader.open(directory2))

        query = QueryParser("contents", analyzer).parse(query_as_text)
        scoreDocs2 = searcher.search(query, hits_per_query).scoreDocs

        finalScoreDocs = interpolate_rankings( [scoreDocs, scoreDocs2], [0.1, 0.9] )
        print(len(scoreDocs))
        runfile_writer(finalScoreDocs, searcher, output_file, query_as_id)



def run4(searcher, analyzer, queries, hits_per_query, output_file):
    from tools import Annotator
    annotator = Annotator()
    queries_text = queries[0]
    queries_ids = queries[1]


    if len(queries_text)!= len(queries_ids):
        print("Query errors")
        exit()
    for i in range(len(queries_text)):
        query_as_text = queries_text[i]
        query_annotation = annotator.getAnnotations(query_as_text)
        named_entities = tag_annotator(query_annotation, "ner")
        query_as_id = queries_ids[i]
        if len(named_entities)!=0:
            query_as_text+=" "
            query_as_text+=" ".join(named_entities)
        query = QueryParser("contents", analyzer).parse(query_as_text)
        scoreDocs = searcher.search(query, hits_per_query).scoreDocs
        print ("%s total matching documents." % len(scoreDocs))
        runfile_writer(scoreDocs, searcher, output_file, query_as_id)



def run6(searcher, analyzer, queries, hits_per_query, output_file, w2v_model):
    #queries = [ [query_text],[query_id]]
    queries_text = queries[0]
    queries_ids = queries[1]
    page_names = queries[2]

    print("Loading w2v Model")
    model = word2vec.load(w2v_model)
    print("Word2Vec model loaded")


    if len(queries_text)!= len(queries_ids):
        print("Query errors")
        exit()

    queryCount = float(len(queries_text))
    
    for i in range(len(queries_text)):
        query_as_text = queries_text[i]
        query_as_id = queries_ids[i]

        tokens = query_as_text.split()
        w2v_tokens = []
        # if not ( "See also" in query_as_text or "External links" in query_as_text or "References" in query_as_text ):
        for t in tokens:
            if t in model:
                w2v_tokens.append(t)

        
        ndx, _ = model.analogy(w2v_tokens, [])
        expansionWords = " ".join([ re.sub("[_|/]", " ", re.sub(r"[\(|\)|'|\"|:]", "", word)) for word in model.vocab[ndx]])
        sys.stdout.write("\r")
        sys.stdout.write("Progress: %f%%  Count: %d" % ( (float(i) / queryCount)*100 , i))
        sys.stdout.flush()

        try:
            query = QueryParser("contents", analyzer).parse(query_as_text + " " + expansionWords)
        except:
            query = QueryParser("contents", analyzer).parse(query_as_text)

        scoreDocs = searcher.search(query, hits_per_query).scoreDocs

        runfile_writer(scoreDocs, searcher, output_file, query_as_id)



def run7(searcher, analyzer, queries, hits_per_query, output_file, w2v_model):
    #queries = [ [query_text],[query_id]]
    queries_text = queries[0]
    queries_ids = queries[1]
    page_names = queries[2]

    print("Loading w2v Model")
    model = word2vec.load(w2v_model)
    print("Word2Vec model loaded")

    if len(queries_text)!= len(queries_ids):
        print("Query errors")
        exit()

    queryCount = float(len(queries_text))
    
    for i in range(len(queries_text)):
        query_as_text = queries_text[i]
        query_as_id = queries_ids[i]

        sys.stdout.write("\r")
        sys.stdout.write("Progress: %f%%  Count: %d" % ( (float(i) / queryCount)*100 , i))
        sys.stdout.flush()

        w2v_tokens = []
        tokens = query_as_text.split()
        for t in tokens:
            if t in model:
                w2v_tokens.append(t)


        queryVecs = [ model[w] for w in w2v_tokens ]

        query = QueryParser("contents", analyzer).parse(query_as_text)
        scoreDocs = searcher.search(query, hits_per_query).scoreDocs

        newRanks = []
        for doc in scoreDocs:
            content = searcher.doc( doc.doc ).get("contents")
            total = 0
            count = 0
            # print(query_as_text)
            # print("&"*40)
            for t in re.findall("[\w-]+", content):
                # len greater than 3 is a braindead removal of stopwords
                if len(t) > 3 and t in model:
                    temp = float("inf")
                    for qVect in queryVecs:
                        temp = min(temp, sum(abs( model[t] - qVect )))
                    # print(t + " -> " + str(temp))
                    total += temp
                    count += 1
            # print("====================================")
            if count > 0:
                newRanks.append( total / count )
            else:
                newRanks.append(float("inf"))

        

        scoreDocs = zip(newRanks, scoreDocs)

        scoreDocs = sorted(scoreDocs, key=lambda x: x[0])
        # print scoreDocs

        scoreDocs = [s[1] for s in scoreDocs]
        runfile_writer(scoreDocs, searcher, output_file, query_as_id)



def interpolate_rankings(rankings, weights):
        '''
            This function takes N rankings and returns an intpolated ranking with
            weights from the weight list of length N
        '''

        docs = {}
        for r in range(len(rankings)):
            rank = 1
            for doc in rankings[r]:
                if doc.doc in docs:
                    docs[doc.doc] += weights[r] * (1.0 / rank)
                else:
                    docs[doc.doc] = weights[r] * (1.0 / rank)
                rank += 1

        docs = [ ScoreDoc(k, v) for k, v in docs.iteritems() ]
        docs = sorted( docs, key=lambda x: -x.score )
        return docs



def runfile_writer(scoreDocs, searcher, output_file, query_as_id):
    rank = 1
    if len(scoreDocs)!=0:
        for doc in [ searcher.doc(x.doc) for x in scoreDocs ]:
            search_result_query = ' '.join([query_as_id, str(0),
                                            doc.get("paraId"),
                                            str(rank),
                                            str(1.0 / rank),
                                            "BBT"])
            output_file.write(search_result_query + "\n")
            rank += 1
    else:
        search_result_query = ' '.join([query_as_id, str(0),
                                        "none",
                                        str(rank),
                                        str(1.0 / rank),
                                        "BBT"])
        output_file.write(search_result_query + "\n")


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


def search_engine_2(queries, hits, k, facet):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run2(searcher, analyzer, queries, hits, run_file, k, facet)
    del searcher
    run_file.close()


def search_engine_5(queries, hits, k):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run5(searcher, analyzer, queries, hits, run_file, k)
    del searcher
    run_file.close()


def search_engine_3(queries, hits):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run3(searcher, analyzer, queries, hits, run_file)
    del searcher
    run_file.close()


def search_engine_4(queries, hits):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run4(searcher, analyzer, queries, hits, run_file)
    del searcher
    run_file.close()



def search_engine_6(queries, hits, w2v_model):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run5(searcher, analyzer, queries, hits, run_file, w2v_model)
    del searcher
    run_file.close()

def search_engine_7(queries, hits, w2v_model):
    run_file = codecs.open("runfile", "w", "utf-8")
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer()
    run6(searcher, analyzer, queries, hits, run_file, w2v_model)
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

import sys,lucene,os
from Indexer_1 import IndexFiles
from Searcher_1 import *
from Queries import read_outline
from Evaluation import eval_result
"""
arg[1]=paragraphs
arg[2]=outline
arg[3]=hirarchical_qrel
arg[4]: 1->baseline model tfidf
        2->top k pseudeo feedback as query model
            arg[5]=top k docs from the pseudo search result are selected
            arg[6] document facet choice from pseudo feedback, it can be "entities", "content"
        4-> give more weights to the entities in the query
        5->arguments A0 and A1 from top-k articles from the pseudo search  result as query expansion
            arg[5]=top k docs from the pseudo search result are selected
paras are indexed in the folder 'BaseIndexFolder'
"""

INDEX_DIR="BaseIndexFolder/"

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.path.join(base_dir, INDEX_DIR)



# indexParas = IndexFiles(sys.argv[1],os.path.join(base_dir, INDEX_DIR))

queries=read_outline(sys.argv[2])
hits_per_query = 200

model = int(sys.argv[4])
if model ==1:
    search_engine_1(queries, hits_per_query)
    eval_result(sys.argv[3])

elif model == 2:
    k = sys.argv[5]
    facet = sys.argv[6]
    search_engine_2(queries, hits_per_query, k, facet)
    eval_result(sys.argv[3])

elif model == 3:
    search_engine_3(queries, hits_per_query)
    eval_result(sys.argv[3])


elif model == 4:
    search_engine_4(queries, hits_per_query)
    eval_result(sys.argv[3])



elif model == 5:
    search_engine_5(queries, hits_per_query, int(sys.argv[5]))
    eval_result(sys.argv[3])

elif model == 6:
    search_engine_6(queries, hits_per_query, sys.argv[5])
    eval_result(sys.argv[3])

elif model == 7:
    search_engine_7(queries, hits_per_query, sys.argv[5])
    eval_result(sys.argv[3])


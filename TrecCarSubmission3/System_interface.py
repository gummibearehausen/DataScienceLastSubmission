from trec_car.read_data import *

import sys,lucene,os
from Indexer_1 import IndexFiles
from Searcher_1 import search_engine_1
from Queries import read_outline
from Evaluation import eval_result
"""
arg[1]=paragraphs
arg[2]=outline
arg[3]=hirarchical_qrel
arg[4]: 1->baseline model tfidf
        2->top k pseudeo feedback as query model
paras are indexed in the folder 'BaseIndexFolder'
"""

INDEX_DIR="BaseIndexFolder/"

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.path.join(base_dir, INDEX_DIR)

indexParas = IndexFiles(sys.argv[1],os.path.join(base_dir, INDEX_DIR))
queries=read_outline(sys.argv[2])
hits_per_query = 2000

model = sys.argv[4]
search_engine_1(queries, hits_per_query, model)
eval_result(sys.argv[3])


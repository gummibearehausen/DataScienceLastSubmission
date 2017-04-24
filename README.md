# DataScienceLastSubmission
pylucene 6.5.0
python 2.7 
numpy

when running the file:
python [paragraphs] [outline] [hierarchical qrel] [model_indictor]

detailed information about the arguments:
arg[1]=paragraphs
arg[2]=outline
arg[3]=hirarchical_qrel
arg[4]: 1->baseline model tfidf
        2->top k pseudeo feedback as query model
        4-> give more weights to the entities in the query
        5->arguments A0 and A1 from top-k articles from the pseudo search  result as query expansion
            arg[5]=top k docs from the pseudo search result are selected
        
paras are indexed in the folder 'BaseIndexFolder'


result:
MAP is for top 1000 search result


Model 1:
MAP: 0.283191417191
P@5: 0.1361003861
p@r: 0.203789292461
MMR: 0.365857122018


model2 contents

MAP: 0.273193549825
P@5: 0.127992277992
p@r: 0.182707296189
MMR: 0.340267582004


model2 entities

MAP: 0.226190895378
P@5: 0.114768339768
p@r: 0.146440191272
MMR: 0.295889908642

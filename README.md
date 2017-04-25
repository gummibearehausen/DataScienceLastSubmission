# DataScienceLastSubmission
pylucene 6.5.0
python 2.7 
numpy

# when running the file:
## python [paragraphs] [outline] [hierarchical qrel] [model_indictor]

# detailed information about the arguments:
# arg[1]=paragraphs
# arg[2]=outline
# arg[3]=hirarchical_qrel
# arg[4]: 
          1->baseline model tfidf
          2->top k pseudeo feedback as query model
                    arg[5]=top k docs from the pseudo search result are selected
                    arg[6] document facet choice from pseudo feedback, it can be "entities", "content"
          4-> give more weights to the entities in the query
          3-> Title Query Integration
          5-> arguments A0 and A1 from top-k articles from the pseudo search  result as query expansion
                    arg[5]=top k docs from the pseudo search result are selected
          6-> Word2Vec Query Expansion
          7-> Word2Vec Reranking
          

        
paras are indexed in the folder 'BaseIndexFolder'


# Method Overviews
## 1. Baseline
This is the baseline which uses the pagename + section path as a query, using TF-IDF as a similarity measure  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 1```
## 2. Pseudo-Feedback
This method takes the content of the top k documents from an initial search and uses that as a query for a second round of searching.  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 2 <k> <contents|entities>```  
*contents* = The entire text from the top k documents is used as a query  
*entities* = Only the entities from the top k documents are used as a query  
## 3. Title Query Integration
This method first uses just the page title as a query, which seems to often contain passages relevent to the article, then uses the title + section path as query. The results of these two searches are then integrated with a weight of 0.1 on the page name query and 0.9 on the full query.  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 3 ```  
## 4. Named Entitiy 
This method first performs named entity recognition on the query, and appends the named entities to the query. This means the query will have double mentions of named entities thus forcing more weight onto those terms.  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 4 ```  
## 5. Pseudorelevence Feedback
Extract the first and the second semantic arguments from the top k pseudo search result, then use those arguments as query expansion. The idea is to explore the theme of the highly -ranked documents

Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 5 <k> ```  
## 6. Word2Vec Query Expansion
This method uses a word2vec model trained on the corpus. All the terms in the query which have an entry in the word2vec model are converted into their vector representation and combined to find a set of most similiar words. These words are then added to the query as an expansion.  
Requires: Running ```word2vec_setup.py <corpus> <output file (ex. corpus-full)>```  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 6 <word2vec model (ex. corpus-full.bin)> ```  
## 7. Word2Vec Reranking
This method first builds a result set of documents using the standard query. A vector for each of the terms in the query is found. Then for each document in the result set: the sum of similarity between each term in the document and the most similiar query term is found. The sum of all similarities is the new ranking for the document.  
Requires: Running ```word2vec_setup.py <corpus> <output file (ex. corpus-full)>```  
Usage: ```python System_interface.py <paragraphs> <outline> <qrel> 7 <word2vec model (ex. corpus-full.bin)> ```  

# Results
## MAP is for top 1000 search result
# results reported here are using test-200


## model 1:
MAP: 0.283191417191  
P@5: 0.1361003861  
p@r: 0.203789292461  
MMR: 0.365857122018  


## model 2 contents

MAP: 0.273193549825  
P@5: 0.127992277992  
p@r: 0.182707296189  
MMR: 0.340267582004  


## model 2 entities

MAP: 0.226190895378  
P@5: 0.114768339768  
p@r: 0.146440191272  
MMR: 0.295889908642  

## model 3
MAP: 0.281396192409  
P@5: 0.133397683398  
p@r: 0.20202368757  
MMR: 0.364631059843  

## model 4
MAP: 0.276497298248  
P@5: 0.131370656371  
p@r: 0.197332226628  
MMR: 0.357580977659  

## model 5
MAP: 0.283143077118  
P@5: 0.1361003861  
p@r: 0.203789292461  
MMR: 0.365850331643  


## Results from indexing half corpus + test200 + 200 hits per query

### Method 1
MAP: 0.144611911874   
P@5: 0.0688223938224  
p@r: 0.109623353641  
MMR: 0.208639018153  

### Method 2, k = 2, contents
MAP: 0.128462499865  
P@5: 0.0625482625483  
p@r: 0.0939533209176  
MMR: 0.182736242051  

### Method 3
MAP: 0.143883007027  
P@5: 0.0676640926641  
p@r: 0.109067394157  
MMR: 0.207625343785  

## Method 4
MAP: 0.138404470225
P@5: 0.0666988416988
p@r: 0.105110230825
MMR: 0.199032216547


### Method 6, Word2Vec Trained using full corpus
MAP: 0.0569984370146  
P@5: 0.0238416988417  
p@r: 0.0419376542591  
MMR: 0.0813393445855  

### Method 7, Word2Vec Trained using full corpus
MAP: 0.0183713101843  
P@5: 0.00492277992278  
p@r: 0.00633068133068  
MMR: 0.0257915772718  

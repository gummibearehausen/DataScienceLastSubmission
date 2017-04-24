#!/usr/bin/env python
# -*- coding: utf-8 -*-


from trec_car.read_data import *
import sys, os, lucene, threading, time
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from  org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, paragraphs, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        print(Paths.get(storeDir))

        analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(), 1048576)
        config = IndexWriterConfig(analyzer)

        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(paragraphs, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, paras, writer):

        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(False)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        with open(paras, 'rb') as f:
            for p in iter_paragraphs(f):
                print('\n', p.para_id, ':')

                # Print just the text
                texts = [elem.text if isinstance(elem, ParaText)
                         else elem.anchor_text
                         for elem in p.bodies]
                # print(' '.join(texts))
                contents = ' '.join(texts)

                # Print just the linked entities
                entities = [elem.page
                            for elem in p.bodies
                            if isinstance(elem, ParaLink)]
                entity_text = '/t'.join(entities)
                'iso-8859-1'

                # Print text interspersed with links as pairs (text, link)
                mixed = [(elem.anchor_text, elem.page) if isinstance(elem, ParaLink)
                         else (elem.text, None)
                         for elem in p.bodies]
                # print(mixed)
                print "adding", p.para_id
                try:
                    doc = Document()
                    doc.add(Field("paraId", p.para_id, t1))
                    doc.add(Field("entities", entity_text, t1))
                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print "warning: no content in %s" % p.para_id
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


                print("*" * 20)



if __name__ == '__main__':
    pass
    # if len(sys.argv) < 2:
    #     print IndexFiles.__doc__
    #     sys.exit(1)
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    # print ('lucene', lucene.VERSION)
    # start = datetime.now()
    # try:
    #     base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    #     print("base_dir " + base_dir)
    #     IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR))
    #
    #     end = datetime.now()
    #     print end - start
    # except Exception, e:
    #     print "Failed: ", e
    #     raise e
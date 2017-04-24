# -*- coding: utf-8 -*-
from tools import Annotator
from pprint import pprint
def tag_annotator(anno, facet):


    if facet =="ner" :
        ne = anno[facet]
        named_entities = []
        temp = ''
        for pair in ne:
            if pair[1][0] == "B":
                temp += pair[0]
            elif pair[1][0] == "I":
                temp += " " + pair[0]
            elif pair[1][0] == "E":
                temp += " " + pair[0]
                named_entities.append(temp)
                temp = " "
        return named_entities

    elif facet == "chunk":
        chunk_pairs = anno[facet]
        chunks = []
        temp = ''
        for pair in chunk_pairs:
            if pair[1][0] == "B" and pair[1][-2:]=="NP" :
                temp += pair[0]
            elif pair[1][0] == "I"and pair[1][-2:]=="NP":
                temp += " " + pair[0]
            elif pair[1][0] == "E"and pair[1][-2:]=="NP":
                temp += " " + pair[0]
                chunks.append(temp)
                temp = " "
        return chunks

def annotator(text, facet):
    anno = Annotator()
    annotation = anno.getAnnotations(text)
    if facet =="ner" :
        ne = annotation['ner']
        named_entities = []
        temp = ''
        for pair in ne:
            if pair[1][0] == "B":
                temp += pair[0]
            elif pair[1][0] == "I":
                temp += " " + pair[0]
            elif pair[1][0] == "E":
                temp += " " + pair[0]
                named_entities.append(temp)
                temp = " "
        return named_entities

    elif facet == "chunk":
        chunk_pairs = annotation[facet]
        chunks = []
        temp = ''
        for pair in chunk_pairs:
            if pair[1][0] == "B" and pair[1][-2:]=="NP" :
                temp += pair[0]
            elif pair[1][0] == "I"and pair[1][-2:]=="NP":
                temp += " " + pair[0]
            elif pair[1][0] == "E"and pair[1][-2:]=="NP":
                temp += " " + pair[0]
                chunks.append(temp)
                temp = " "
        return chunks



if __name__ == "__main__":
    text = " Bill Clinton is shaking handing with Barack Obama"
    ne = annotator(text,"chunk")
    named_entities = []
    temp=''
    pprint(ne)
    # for pair in ne:
    #     if pair[1][0]=="B":
    #         temp+=pair[0]
    #     elif pair[1][0] =="I":
    #         temp += " "+ pair[0]
    #     elif pair[1][0] =="E":
    #         temp += " " + pair[0]
    #         named_entities.append(temp)
    #         temp =" "
    # print(named_entities)

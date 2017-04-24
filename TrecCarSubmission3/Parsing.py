# -*- coding: utf-8 -*-
from tools import Annotator

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
    else:
        args_total = []
        if anno:
            srl_annotation = anno["srl"]
            key_sets = {"A1", "A0"}

            if len(srl_annotation)!=0:
                for each_annotation in srl_annotation:
                    if len(each_annotation)!=0:
                        args = [each_annotation[arg_key] for arg_key in key_sets if arg_key in each_annotation]
                        args_total += args
        if len(args_total)!=0:
            s = " ".join(args_total)
            return s
        else:
            s = " "
            return s


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
    pass




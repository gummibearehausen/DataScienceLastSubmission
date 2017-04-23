# -*- coding: utf-8 -*-
from SemanticRoleLabeling.tools import Annotator
from pprint import pprint

anno = Annotator()
text = "In the eastern provinces of Banat and Transylvania (German: Siebenbürgen), German was the predominant language not only in the larger towns – such as Temeswar (Timișoara), Hermannstadt (Sibiu) and Kronstadt (Brașov) – but also in many smaller localities in the surrounding areas"
text_2 = "In 1901, the 2nd Orthographical Conference ended with a complete standardization of the German language in its written form and the Duden Handbook was declared its standard definition"

annotation = anno.getAnnotations(text_2.split(".")[0])
pprint(text_2.split(".")[0])
pprint(annotation['ner'])
pprint(annotation['srl'])
pprint(annotation['chunk'])
pprint(annotation)

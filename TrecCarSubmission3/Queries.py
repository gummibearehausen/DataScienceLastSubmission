from trec_car.read_data import *
import re


def read_outline(outlines):
    hierarchical_headings =[]
    hierarchical_headings_ids =[]
    page_names = []
    with open(outlines, 'rb') as f:
        for p in iter_annotations(f):
            # print('\npagename:', p.page_name)

            # get one data structure with nested (heading, [children]) pairs
            headings = p.nested_headings()
            # print(headings)

            if len(p.outline())>2:
                print('heading 1=', p.outline()[0].heading)

            # print('deep headings= ', len(p.deep_headings_list()))
            #
            # print('flat headings= ', p.flat_headings_list())


            for headings in p.flat_headings_list():
                hier_heading_id = p.page_id+"/"+"/".join([child.headingId for child in headings])
                hier_heading_text=p.page_name+" "+" ".join([re.sub(r'[^A-Za-z0-9]',' ',child.heading) for child in headings])

                hierarchical_headings.append(hier_heading_text)
                hierarchical_headings_ids.append(hier_heading_id)
                page_names.append( p.page_name )
                # print(".........")
    output = list([hierarchical_headings,hierarchical_headings_ids, page_names])
    return output

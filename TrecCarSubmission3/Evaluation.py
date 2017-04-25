import codecs
from collections import defaultdict
import numpy as np


def query_rank_list(file_name_1, file_name_2):
    query_truth_set = read_qrel_file(file_name_2)
    #print("number of queries in the qrel is: " + str(len(query_truth_set.keys())))
    query_ranklist = defaultdict(list)
    with codecs.open(file_name_1) as runfile:
        for line in runfile:
            parsed_line = line.strip().split()
            query_id = parsed_line[0]
            passage_id = parsed_line[2]
            if query_id in query_truth_set:
                if passage_id in query_truth_set[query_id]:
                    query_ranklist[query_id].append(1)
                else:
                    query_ranklist[query_id].append(0)
    query_true_para_num = [len(query_truth_set[q]) for q in query_ranklist.keys()]
    return [query_true_para_num, query_ranklist.values()]


def read_qrel_file(file_name):
    query_truth = defaultdict(set)
    with codecs.open(file_name) as qrel:
        for line in qrel:
            parsed_line = line.strip().split()
            query_id = parsed_line[0]
            passage_id = parsed_line[2]
            query_truth[query_id].add(passage_id)
    return query_truth


def eval_result(qrel_file_name):
    run_file_name = "runfile"
    return_result = query_rank_list(run_file_name,qrel_file_name)
    true_para_num_per_query_list = return_result[0]
    ranklist_per_query_list = return_result[1]


    num_of_query = len(true_para_num_per_query_list)
    #print("number of queries in the runfile is: " + str(num_of_query))
    map_total = []
    prec_at_r_total = []
    prec_at_5_total = []
    mrr_total = []
    for q in range(num_of_query):
        true_para_num = true_para_num_per_query_list[q]
        r = ranklist_per_query_list[q]
        if len(r)>1000:
            r_prime = r[:1000]
            r = r_prime
        rank_list = np.array(r)
        rel_indices = rank_list.nonzero()
        if len(rel_indices[0]) != 0:
            map = np.sum([1.0*(list(rel_indices[0]).index(i)+1) / (float(i) + 1) for i in rel_indices[0]]) / float(true_para_num)
            prec_at_5 = np.sum(rank_list[:5]) / 5.0
            prec_at_R = np.sum(rank_list[:true_para_num]) / float(true_para_num)
            mrr = 1.0 /(rel_indices[0][0] + 1)

            prec_at_5_total.append(prec_at_5)
            prec_at_r_total.append(prec_at_R)
            map_total.append(map)
            mrr_total.append(mrr)

    map_ave = np.sum(map_total) / float(num_of_query)
    precision_average_queries = np.sum(prec_at_5_total) / float(num_of_query)
    precision_at_r_average_queries = np.sum(prec_at_r_total) / float(num_of_query)
    mrr_average_queries =np.sum(mrr_total)/float(num_of_query)
    eval = [map_ave,
            precision_average_queries,
            precision_at_r_average_queries,
            mrr_average_queries]
    s = ""
    s+="MAP: " + str(eval[0])+"\n"
    s+="P@5: " + str(eval[1])+"\n"
    s+="p@r: " + str(eval[2])+"\n"
    s+="MMR: " + str(eval[3])+"\n"
    print(s)

if __name__ == '__main__':
    pass

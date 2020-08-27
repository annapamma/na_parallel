import pickle
import random
import os
import sys

# steps:
# pull out ppi as dictionary
# get all genes from ppi
# pull out pathway db
# select random set of x genes (gene-set)
# for each gene in random set of x genes, find overlap between pathway and gene set
# add overlap to list to create distribution

# pw_db_name = sys.argv[1]
# random_gene_length = sys.argv[2]
pw_db_name = 'xcell'
random_gene_length = 10


def k_neighbors_v_occurrences(pw_genes, random_gene_len):
    pw_counts = {}
    for dist_length in range(1, 100001):
        if dist_length % 10000 == 0:
            print(pw, '-', random_gene_len, ' : ', dist_length)
        random.seed(dist_length)
        random_genes = set(random.sample(all_genes, random_gene_len))
        neighbor_len = sum(
            [
                len(pw_genes.intersection(ppi_dict[g]))
                for g in random_genes
            ]
        )
        if neighbor_len not in pw_counts:
            pw_counts[neighbor_len] = 0
        pw_counts[neighbor_len] += 1
    return pw_counts


ppi = pickle.load(open('/Users/anna/PycharmProjects/na_parallel/downloads/BIOGRID_dl_aug2220.pkl', 'rb'))
ppi_dict = ppi['ppi_dict']
all_genes = ppi['all_genes']

pw_db = pickle.load(open(f'./databases/{pw_db_name}.pkl', 'rb'))

with open("./tmp/tests-to-run") as pathways_to_run:
    pws = pathways_to_run.read().split("\n")
    for pw in pws:
        with open(pw) as pw_f:
            gene_str = pw_f.read()
            genes = set(gene_str.split('\t'))
        pw_dist = k_neighbors_v_occurrences(
            pw_genes=genes,
            random_gene_len=random_gene_length
        )
        output_dir = f'./distributions/{pw}'
        output_f = f'{output_dir}/{random_gene_length}'
        os.makedirs(output_dir, exist_ok=True)
        pickle.dump(pw_dist, open(output_f, 'wb'))
        print('finished: ', output_f)
        break

# for pw, genes in pw_db.items():
#     pw_counts[pw] = {}
#     print('starting pw: ', pw)
#     for dist_length in range(1, 1000001):
#         print(pw, ' : ', dist_length)
#         random.seed(dist_length)
#         random_genes = set(random.sample(all_genes, random_genes_len))
#         neighbor_len = sum(
#             [
#                 len(genes.intersection(ppi_dict[g]))
#                 for g in set(random.sample(all_genes, random_genes_len))
#             ]
#         )
#         if neighbor_len not in pw_counts[pw]:
#             pw_counts[pw][neighbor_len] = 0
#         pw_counts[pw][neighbor_len] += 1
#
#     pickle.dump(pw_counts, open(f'./distributions/{pw_db_name}/{}/{random_genes_len}.pkl', 'wb'))


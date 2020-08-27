import pickle

pw_dbs = ['kegg', 'reactome', 'xcell']

for db_name in pw_dbs:
    pw_db = pickle.load(open(f'/Users/anna/PycharmProjects/na_parallel/databases/{db_name}.pkl', 'rb'))

    for pw, genes in pw_db.items():
        if '/' in pw:
            pw = '-'.join(pw.split('/'))
        with open(f'{db_name}/{pw}.txt', 'w') as f:
            f.write('\t'.join(genes))
        print(f'finished: {db_name} - {pw}')

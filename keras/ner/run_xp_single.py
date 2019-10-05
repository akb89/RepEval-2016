from __future__ import print_function

import sys
from collections import defaultdict

import mlp


def process_file(datasets, filepath):
    tmp_results_log = defaultdict(defaultdict)
    model_name_log = filepath.split('/')[-1].split('.npy')[0]
    for dataset in datasets:
        if dataset.split('/')[-1] == 'CoNLL00':
            dataset_name_log = 'conll00'
        elif dataset.split('/')[-1] == 'CoNLL03':
            dataset_name_log = 'conll03'
        elif dataset.split('/')[-1] == 'PTB-pos':
            dataset_name_log = 'ptb'
        else:
            raise Exception('ERROR parsing dataset name')
        tmp_results_dict = mlp.run_mlp(filepath, dataset, model_name_log, dataset_name_log)
        for model_name, results in tmp_results_dict.items():
            for result in results:
                tmp_results_log[model_name][result] = tmp_results_dict[model_name][result]
    return tmp_results_log


if __name__ == '__main__':
    datasets = sys.argv[1:3]
    filepath = sys.argv[3]
    tmp_results_log = process_file(datasets, filepath)
    for model_name, results in tmp_results_log.items():
        print('Completed model = {}'.format(model_name))
        print('Results = {}'.format(results))
        print('{}\t{}\t{}\t{}\t{}'.format(
                model_name, results['conll00'], results['conll03'],
                results['conll00-oov'], results['conll03-oov']), file=sys.stderr)

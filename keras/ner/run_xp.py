import sys
import multiprocessing
import functools
from contextlib import closing
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
    datasets = sys.argv[1:4]
    files = sys.argv[4:]
    results_log = defaultdict(defaultdict)
    process = functools.partial(process_file, datasets)
    with closing(multiprocessing.Pool(50)) as pool:
        for tmp_results_log in pool.imap_unordered(process, files):
            for model_name, results in tmp_results_log.items():
                for result in results:
                    results_log[model_name][result] = tmp_results_log[model_name][result]
    with open('results.txt', 'w') as output_stream:
        print >> output_stream, 'MODEL\tCONLL00\tCONLL03\tPTB\tCONLL00-OOV\tCONLL03-OOV\tPTB-OOV'
        for model_name, results in sorted(results_log.items()):
            print(model_name)
            print >> output_stream, '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                model_name, results['conll00'], results['conll03'], results['ptb'],
                results['conll00-oov'], results['conll03-oov'], results['ptb-oov'])

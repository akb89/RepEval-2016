import sys
import multiprocessing
import functools
from contextlib import closing
from collections import defaultdict

from tqdm import tqdm

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
    with open('results.txt', 'w') as output_stream:
        with closing(multiprocessing.Pool(30)) as pool:
            for tmp_results_log in tqdm(pool.imap_unordered(process, files), total=len(files)):
                for model_name, results in tmp_results_log.items():
                    print >> output_stream, '{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                        model_name, results['conll00'], results['conll03'], results['ptb'],
                        results['conll00-oov'], results['conll03-oov'], results['ptb-oov'])

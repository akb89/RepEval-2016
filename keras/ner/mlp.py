#!/usr/bin/env python

import sys
import numpy as np

from os import path
from logging import info, warn
from collections import defaultdict

from keras.models import Sequential
from keras.layers import Reshape, Dense, Activation
from keras.layers import Merge, Flatten
from keras import optimizers
from layers import Input, FixedEmbedding

import input_data
import common
import settings

# Settings

class Defaults(object):
    window = 2
    max_vocab_size = None
    max_train_examples = None
    max_develtest_examples = 100000    # for faster develtest
    examples_as_indices = True
    hidden_sizes = [300]
    hidden_activation = 'hard_sigmoid' # 'relu'
    batch_size = 50
    epochs = 10
    loss = 'categorical_crossentropy' # 'mse'
    verbosity = 1    # 0=quiet, 1=progress bar, 2=one line per epoch
    iobes = False     # Map tags to IOBES on input
    token_level_eval = False    # Token-level eval even if IOB-like tagging
    optimizer = 'adam' # 'sgd'
    test = True
    format = 'numpy'

def run_mlp(filepath, dataset, model_name_log, dataset_name_log):
    # config = settings.from_cli(['datadir', 'wordvecs'], Defaults)
    config = Defaults()
    config.datadir = dataset
    config.wordvecs = filepath
    config.results_log = defaultdict(defaultdict)
    config.model_name_log = model_name_log
    config.dataset_name_log = dataset_name_log
    optimizer = optimizers.get(config.optimizer)
    output_name = 'mlp--' + path.basename(config.datadir.rstrip('/'))
    #common.setup_logging(output_name)
    #settings.log_with(config, info)
    print('Processing model: {} on dataset: {}'.format(
        model_name_log, dataset_name_log))

    # Data
    data = input_data.read_data_sets(config.datadir, config.wordvecs, config)
    embedding = common.word_to_vector_to_matrix(config.word_to_vector)

    if config.max_train_examples and len(data.train) > config.max_train_examples:
        warn('cropping train data from %d to %d' % (len(data.train),
                                                    config.max_train_examples))
        data.train.crop(config.max_train_examples)

    # Model
    model = Sequential()

    # Separate embedded-words and word-features sequences
    embedded = Sequential()
    embedded.add(FixedEmbedding(embedding.shape[0], embedding.shape[1],
                                input_length=data.input_size, weights=[embedding]))
    features = Sequential()
    features.add(Input(data.feature_shape))

    model.add(Merge([embedded, features], mode='concat', concat_axis=2))
    model.add(Flatten())

    # Fully connected layers
    for size in config.hidden_sizes:
        model.add(Dense(size))
        model.add(Activation(config.hidden_activation))
    model.add(Dense(data.output_size))
    model.add(Activation('softmax'))

    model.compile(optimizer=optimizer, loss=config.loss)

    def predictions(model, inputs):
        output = list(model.predict(inputs, batch_size=config.batch_size))
        return np.argmax(np.asarray(output), axis=1)

    def eval_report(prefix, model, dataset, config, log=info):
        pred = predictions(model, dataset.inputs)
        gold = np.argmax(dataset.labels, axis=1)
        summary = common.performance_summary(dataset.words, gold, pred, config)
        # for s in summary.split('\n'):
        #     log(prefix + ' ' + s)

    # small_train = data.train.subsample(config.max_develtest_examples)
    # small_devel = data.devel.subsample(config.max_develtest_examples)

    for epoch in range(1, config.epochs+1):
        model.fit(data.train.inputs, data.train.labels,
                  batch_size=config.batch_size, nb_epoch=1,
                  verbose=config.verbosity)
        # eval_report('Ep %d train' % epoch, model, small_train, config)
        # eval_report('Ep %d devel' % epoch, model, small_devel, config)
        data.train.shuffle()

    # eval_report('FINAL train', model, data.train, config)
    # eval_report('FINAL devel', model, data.devel, config)

    # pred = predictions(model, data.devel.inputs)
    # common.save_gold_and_prediction(data.devel, pred, config, output_name)

    if config.test:
        eval_report('TEST', model, data.test, config)
        pred = predictions(model, data.test.inputs)
        common.save_gold_and_prediction(data.test, pred, config,
                                        'TEST--' + output_name)
    return config.results_log

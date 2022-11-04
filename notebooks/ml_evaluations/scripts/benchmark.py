import pandas as pd
import numpy as np
import json
import argparse
from ast import literal_eval

from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split

import lightgbm as lgb

from keras_preprocessing.sequence import pad_sequences


import warnings
warnings.filterwarnings('ignore')
from utils import log_msg, precision_reall_f1_report
from models import shallow_NN, vanilla_LSTM, pat_LSTM, CustomStopper, keras_categorical


def get_f1_threshold(y_true, y_pred):

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
    reports = precision_reall_f1_report(precision, recall, thresholds,
                                        plot=False)

    return reports[reports['f1'] == reports['f1'].max()]['threshold'].values[0]


def prediction_scores(y_true, y_prob, threshold=0.5):
    metrics_dict = {}

    metrics_dict['auc'] = roc_auc_score(y_test, y_prob)

    y_pred_label = [1 if i >= threshold else 0 for i in y_prob]
    metrics_dict['f1'] = f1_score(y_test, y_pred_label)
    metrics_dict['precision'] = precision_score(y_test, y_pred_label)
    metrics_dict['recall'] = recall_score(y_test, y_pred_label)

    return metrics_dict




def evaluate_algo(X_train, y_train, X_test, y_test, algo, params,
                  valid_size=0.1, random_state=123456):
    """
    Benchmark algorithms.

    :param X_train: DataFrame, train data features
    :param y_train: DataFrame, train labels
    :param X_test: DataFrame, test data features
    :param y_test: DataFrame, test labels
    :param algo: str, the algorithm to be evaluated.
    :param params: Dict[str, double], algorithm specific params.
    :return results: DataFrame, columns :  "algo", "metric", "value"
    """

    if "lightgbm" in algo.lower():
        algo_params = params[algo.lower()]
        X_train_final, X_valid, y_train_final, y_valid = train_test_split(X_train, y_train,
                                                                          test_size=valid_size,
                                                                          random_state=random_state)

        train_params = {'objective': algo_params['objective'],
                        'num_iterations': algo_params['num_iterations'],
                        'n_jobs': algo_params['n_jobs'],
                        'random_state': random_state,
                        "metric": algo_params['metric'],
                        'verbosity': algo_params['verbosity']
                        }

        dtrain = lgb.Dataset(X_train_final, label=y_train_final)
        dvalid = lgb.Dataset(X_valid, label=y_valid)

        log_msg(">>> Training " + algo.lower())
        model = lgb.train(train_params, dtrain, valid_sets = [dvalid], verbose_eval=algo_params['verbose_eval'],
                          early_stopping_rounds=algo_params['early_stopping_rounds'])
        log_msg(">>> Finished!")

        y_pred = model.predict(X_valid)
        threshold = get_f1_threshold(y_valid, y_pred)

        y_pred = model.predict(X_test)
        metrics_dict = prediction_scores(y_test, y_pred, threshold=threshold)

    elif "shallow_nn" in algo.lower():

        algo_params = params[algo.lower()]
        X_train_final, X_valid, y_train_final, y_valid = train_test_split(X_train, y_train,
                                                                          test_size=valid_size,
                                                                          random_state=random_state)
        columns = X_train.columns

        X_train_final = X_train_final.values
        X_valid = X_valid.values
        y_train_final = y_train_final.values
        y_valid = y_valid.values

        model = shallow_NN(len(columns), algo_params['num_classes'],
                           layer_nodes=algo_params['layer_nodes'])

        early_stop = CustomStopper(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='min',
                                   start_epoch=algo_params['early_stop_start'],
                                   restore_best_weights=True)

        y_train_final_categorical = keras_categorical(y_train_final, algo_params['num_classes'])
        y_valid_categorical = keras_categorical(y_valid, algo_params['num_classes'])

        log_msg(">>> Training " + algo.lower())
        model.fit(X_train_final, y_train_final_categorical,
                  batch_size=algo_params['batch_size'],
                  epochs=algo_params['max_epochs'],
                  validation_data=(X_valid, y_valid_categorical),
                  verbose=algo_params['verbose'],
                  callbacks=[early_stop])
        log_msg(">>> Finished!")

        y_pred = model.predict(X_valid)
        y_pred = y_pred[:, 1]
        threshold = get_f1_threshold(y_valid, y_pred)

        y_pred = model.predict(X_test)
        y_pred = y_pred[:, 1]
        metrics_dict = prediction_scores(y_test, y_pred, threshold=threshold)

    elif "vanilla_lstm" in algo.lower():

        algo_params = params[algo.lower()]

        X_train = X_train['sequence'].apply(lambda x: [int(i) for i in literal_eval(x)]).values
        X_train = pad_sequences(X_train, maxlen=algo_params['input_len'])

        X_test = X_test['sequence'].apply(lambda x: [int(i) for i in literal_eval(x)]).values
        X_test = pad_sequences(X_test, maxlen=algo_params['input_len'])

        y_train = y_train.values
        y_test = y_test.values

        X_train_final, X_valid, y_train_final, y_valid = train_test_split(X_train, y_train,
                                                                          test_size=valid_size,
                                                                          random_state=random_state)

        vocab_size = np.max(X_train) + 1

        model = vanilla_LSTM(vocab_size, algo_params['embedding_dim'],
                             algo_params['num_lstm_units'],
                             algo_params['input_len'], algo_params['num_classes'],
                             layer_nodes=algo_params['layer_nodes'])

        early_stop = CustomStopper(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='min',
                                   start_epoch=algo_params['early_stop_start'],
                                   restore_best_weights=True)

        y_train_final_categorical = keras_categorical(y_train_final, algo_params['num_classes'])
        y_valid_categorical = keras_categorical(y_valid, algo_params['num_classes'])

        log_msg(">>> Training " + algo.lower())
        model.fit(X_train_final, y_train_final_categorical,
                  batch_size=algo_params['batch_size'],
                  epochs=algo_params['max_epochs'],
                  validation_data=(X_valid, y_valid_categorical),
                  verbose=algo_params['verbose'],
                  callbacks=[early_stop])
        log_msg(">>> Finished!")

        y_pred = model.predict(X_valid)
        y_pred = y_pred[:, 1]
        threshold = get_f1_threshold(y_valid, y_pred)

        y_pred = model.predict(X_test)
        y_pred = y_pred[:, 1]
        metrics_dict = prediction_scores(y_test, y_pred, threshold=threshold)

    elif "lstm_seq_feature" in algo.lower():

        algo_params = params[algo.lower()]

        X_test_seq = X_test['sequence'].apply(lambda x: [int(i) for i in literal_eval(x)]).values
        X_test_seq = pad_sequences(X_test_seq, maxlen=algo_params['input_len'])
        X_test_pat = X_test.drop(['sequence'], axis=1).values

        y_train = y_train.values
        y_test = y_test.values

        X_train_final, X_valid, y_train_final, y_valid = train_test_split(X_train, y_train,
                                                                          test_size=valid_size,
                                                                          random_state=random_state)

        X_train_final_seq = X_train_final['sequence'].apply(lambda x: [int(i) for i in literal_eval(x)]).values
        X_train_final_seq = pad_sequences(X_train_final_seq, maxlen=algo_params['input_len'])

        X_valid_seq = X_valid['sequence'].apply(lambda x: [int(i) for i in literal_eval(x)]).values
        X_valid_seq = pad_sequences(X_valid_seq, maxlen=algo_params['input_len'])

        X_train_final_pat = X_train_final.drop(['sequence'], axis=1).values
        X_valid_pat = X_valid.drop(['sequence'], axis=1).values

        vocab_size = np.max(X_train_final_seq) + 1
        num_pat_features = X_train_final_pat.shape[1]

        model = pat_LSTM(vocab_size, algo_params['embedding_dim'],
                         algo_params['num_lstm_units'],
                         algo_params['input_len'],
                         num_pat_features,
                         algo_params['num_classes'],
                         layer_nodes=algo_params['layer_nodes'])

        early_stop = CustomStopper(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='min',
                                   start_epoch=algo_params['early_stop_start'],
                                   restore_best_weights=True)

        y_train_final_categorical = keras_categorical(y_train_final, algo_params['num_classes'])
        y_valid_categorical = keras_categorical(y_valid, algo_params['num_classes'])

        log_msg(">>> Training " + algo.lower())
        model.fit([X_train_final_seq, X_train_final_pat], y_train_final_categorical,
                  batch_size=algo_params['batch_size'],
                  epochs=algo_params['max_epochs'],
                  validation_data=([X_valid_seq, X_valid_pat], y_valid_categorical),
                  verbose=algo_params['verbose'],
                  callbacks=[early_stop])
        log_msg(">>> Finished!")

        y_pred = model.predict([X_valid_seq, X_valid_pat])
        y_pred = y_pred[:, 1]
        threshold = get_f1_threshold(y_valid, y_pred)

        y_pred = model.predict([X_test_seq, X_test_pat])
        y_pred = y_pred[:, 1]
        metrics_dict = prediction_scores(y_test, y_pred, threshold=threshold)

    results = []
    for metric in metrics_dict.keys():
        results.append({'algo': algo.lower(),
                        'metric': metric,
                        'value': metrics_dict[metric]})

    results_df = pd.DataFrame(results)

    return results_df


if __name__ == '__main__':
    """
    Usage example: python benchmark.py --settings benchmark_settings.json
    
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", help="Benchmark settings", type=str, default='benchmark_settings.json')
    
    script_args = parser.parse_args()
    script_args = vars(script_args)
    
    with open(script_args['settings'], 'r') as f:
        args = json.load(f)
    
    data = pd.read_csv(args['data'])

    results = []
    algorithms = list(args['params'].keys())

    for i in range(args['num_bootstrap']):

        log_msg(">>> Bootstrap --  " + str(i))

        seed = args['seed'] + i * 2

        for algo in algorithms:

            if "lightgbm" in algo.lower() or "shallow_nn" in algo.lower():
                X_train, X_test, y_train, y_test = train_test_split(data.drop(['sequence', 'label'], axis=1),
                                                                    data[['label']],
                                                                    test_size=args['test_size'],
                                                                    random_state=seed)
            elif "vanilla_lstm" in algo.lower():
                X_train, X_test, y_train, y_test = train_test_split(data[['sequence']],
                                                                    data[['label']],
                                                                    test_size=args['test_size'],
                                                                    random_state=seed)
            elif "lstm_seq_feature" in algo.lower():
                X_train, X_test, y_train, y_test = train_test_split(data.drop(['label'], axis=1),
                                                                    data[['label']],
                                                                    test_size=args['test_size'],
                                                                    random_state=seed)

            res = evaluate_algo(X_train, y_train, X_test, y_test, algo, args['params'],
                                valid_size=args['valid_size'], random_state=seed)

            results.append(res)

    results_df = pd.concat(results)
    results_df.to_csv(args['results_file'], index=False)

















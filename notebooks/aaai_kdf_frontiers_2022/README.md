# Evaluations of ML models using Seq2Pat features
This directory contains the source code and notebooks to train and evaluate various ML models using Seq2Pat features. 
This source repo has been used to implement the experiments in our papers:
* [[AAAI-IAAI'22] Seq2Pat: Sequence-to-Pattern Generation for Constraint-based Sequential Pattern Mining](https://ojs.aaai.org/index.php/AAAI/article/view/21542),
* [[KDF'22] Dichotomic Pattern Mining with Applications to Intent Prediction from Semi-Structured Clickstream Datasets](https://arxiv.org/abs/2201.09178),
* [[Frontiers in AI 2022] Dichotomic Pattern Mining Integrated With Constraint Reasoning for Digital Behavior Analysis](https://www.frontiersin.org/articles/10.3389/frai.2022.868085/full).

## Running on sample data
We are running on the same sample dataset that has been introduced in the `dichotomic_pattern_mining` notebook, while the generated features are combined with the original sequences data for training the downstream ML models.
The new sample dataset containing features can be found in the `data` folder.

## Requirements
Please run `pip install -r -q requriements.txt` to install the packages used in the source codes and notebooks.

## Compared ML models
Please find the notebooks that are provided under the `notebooks` directory, to see how the following models using different combinations of features are trained and evaluated:

| MODEL      | FEATURE SPACE |
| ----------- | ----------- |
| LightGBM     | Seq2Pat Patterns       |
| Shallow_NN   | Seq2Pat Patterns       |
| LSTM   | Clickstream       |
| LSTM_seq2pat  | Clickstream + Seq2Pat Patterns       |

`scripts/benchmark.py` provides the implementations to run on multiple times of train/test data partition, in order to compare the averaged performances of above models.



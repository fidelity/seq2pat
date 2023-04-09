[![ci](https://github.com/fidelity/seq2pat/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/fidelity/seq2pat/actions/workflows/ci.yml) [![PyPI version fury.io](https://badge.fury.io/py/seq2pat.svg)](https://pypi.python.org/pypi/seq2pat/) [![PyPI license](https://img.shields.io/pypi/l/seq2pat.svg)](https://pypi.python.org/pypi/seq2pat/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Downloads](https://static.pepy.tech/personalized-badge/seq2pat?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/seq2pat)


Seq2Pat: Sequence-to-Pattern Generation Library
===============================================

Seq2Pat ([AAAI'22](https://ojs.aaai.org/index.php/AAAI/article/view/21542)) is a research library for sequence-to-pattern generation to discover
sequential patterns that occur frequently in large sequence databases.
The library supports constraint-based reasoning to specify
desired properties over patterns.

Dichomotic Pattern Mining ([KDF@AAAI'22](https://arxiv.org/abs/2201.09178), [Frontiers'22](https://www.frontiersin.org/articles/10.3389/frai.2022.868085/full)) embeds Seq2Pat to exploit the dichotomy of positive vs. negative outcomes in populations. This allows  constraint-based sequence analysis to generate patterns that uniquely distinguishes cohorts. These patterns can be turned into feature vectors to feed into machine learning models for downstream tasks, e.g., intent prediction, intruder detection, and more generally, for digital behavior analysis. 

From an algorithmic perspective, the library takes advantage of
[multi-valued decision diagrams (AAAI'19)](https://aaai.org/ojs/index.php/AAAI/article/view/3962).

From an implementation perspective, the library is written in ```Cython```
that brings together the efficiency of a low-level ```C++``` backend and
the expressiveness of a high-level ```Python``` public interface.

Seq2Pat is developed as a joint collaboration between Fidelity Investments
and the Tepper School of Business at CMU. Documentation is available at [fidelity.github.io/seq2pat](https://fidelity.github.io/seq2pat).

## Quick Start

We present examples for constraint-based sequential pattern mining and dichotomic pattern mining. 
Sequences can be represented as strings or positive integers.

### Constraint-based Sequential Pattern Mining
```python
# Example to show how to find frequent sequential patterns
# from a given sequence database subject to constraints
from sequential.seq2pat import Seq2Pat, Attribute

# Seq2Pat over 3 sequences
seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                             ["C", "B", "A"],
                             ["C", "A", "C", "D"]])

# Price attribute corresponding to each item
price = Attribute(values=[[5, 5, 3, 8, 2],
                          [1, 3, 3],
                          [4, 5, 2, 1]])

# Average price constraint
seq2pat.add_constraint(3 <= price.average() <= 4)

# Patterns that occur at least twice (A-D)
patterns = seq2pat.get_patterns(min_frequency=2)
```

### Dichotomic Pattern Mining
```python
# Example to show how to run Dichotomic Pattern Mining 
# on sequences with positive and negative outcomes
from sequential.seq2pat import Seq2Pat
from sequential.pat2feat import Pat2Feat
from sequential.dpm import dichotomic_pattern_mining, DichotomicAggregation

# Create seq2pat model for positive sequences
sequences_pos = [["A", "A", "B", "A", "D"]]
seq2pat_pos = Seq2Pat(sequences=sequences_pos)

# Create seq2pat model for negative sequences
sequences_neg = [["C", "B", "A"], ["C", "A", "C", "D"]]
seq2pat_neg = Seq2Pat(sequences=sequences_neg)

# Run DPM to mine patterns that are aggregated as the 
# union, intersection, or the unique patterns among positive and negative sequences
aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg, 
                                                    min_frequency_pos=1, 
                                                    min_frequency_neg=2)

# DPM patterns with union aggregation of positive and negative patterns
# see also intersection, unique_pos, and unique_neq
dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

# Most interestingly, we can generate features from DRPM patterns (pat2feat) 
# to create machine learning models in downstream tasks, e.g., intent prediction
# To do that, we can the input sequences into one-hot feature vectors 
# Binary features denote existence of found patterns in each sequence
pat2feat = Pat2Feat()
sequences = sequences_pos + sequences_neg
encodings = pat2feat.get_features(sequences, dpm_patterns, drop_pattern_frequency=False)

# These encodings can be used as feature vectors in ML models
# to predict the positive vs. negative labels in the dataset
```

## Available Constraints

The library offers various constraint types, including a number of non-monotone constraints.

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.
* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.
* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.
* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

## Usage Examples

Examples on how to use the available constraints can be found 
in the [Usage Example Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/sequential_pattern_mining.ipynb).
You can also find out how to scale up the mining capability, by running Seq2Pat on batches of sequences in parallel in [Batch Processing Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/batch_processing.ipynb). 

Supported by Seq2Pat, we proposed **Dichotomic Pattern Mining** ([X. Wang and S. Kadioglu, 2022](https://arxiv.org/abs/2201.09178)) to analyze the correlations between 
mined patterns and different outcomes of sequences. DPM allows generating feature vectors based on mined patterns and plays an integrator role between Sequential 
Pattern Mining and the downstream modeling tasks as shown in [Ghosh et. al., Frontiers'22](https://www.frontiersin.org/articles/10.3389/frai.2022.868085/full) for clickstream intent prediction and intruder detection. An example on how to run DPM and generate pattern embeddings can be found in 
[Dichotomic Pattern Mining Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/dichotomic_pattern_mining.ipynb).

## Installation

Seq2Pat can be installed from PyPI using ``pip install seq2pat``. It can also be installed from source by following the instructions in
our [documentation](https://fidelity.github.io/seq2pat/installation.html).

### Requirements

The library requires ```Python 3.7+```, the ```Cython``` package, and a ```C++``` compiler.
See [requirements.txt](requirements.txt) for dependencies.

## Support

Please submit bug reports, questions and feature requests as [Issues](https://github.com/fidelity/seq2pat/issues).

## Citation

If you use Seq2Pat in a publication, please cite it as:

```bibtex
  @article{seq2pat2022,
    title={Seq2Pat: Sequence-to-Pattern Generation for Constraint-based Sequential Pattern Mining},
    author={Wang Xin, Hosseininasab Amin, Colunga Pablo, Kadioglu Serdar, van Hoeve Willem-Jan},
    journal={Proceedings of the AAAI Conference on Artificial Intelligence},
    url={https://ojs.aaai.org/index.php/AAAI/article/view/21542},
    volume={36},
    number={11},
    pages={12665-12671},
    year={2022}
  }
```

To cite the Dichotomic Pattern Mining framework, please cite it as:

```bibtex
  @article{Frontiers2022,
    title={Dichotomic Pattern Mining Integrated with Constraint Reasoning for Digital Behaviour Analyses}, 
    author={Sohom Ghosh, Shefali Yadav, Xin Wang, Bibhash Chakrabarty, Serdar Kadioglu},
    journal={Frontiers in Artificial Intelligence},
    url={https://www.frontiersin.org/articles/10.3389/frai.2022.868085},
    volume={5},
    year={2022}    
}
```

```bibtex
@inproceedings{DPM2022,
    title={Dichotomic Pattern Mining with Applications to Intent Prediction from Semi-Structured Clickstream Datasets}, 
    author={Xin Wang and Serdar Kadioglu},
    booktitle={The AAAI-22 Workshop on Knowledge Discovery from Unstructured Data in Financial Services},
    publisher={arXiv},
    url={https://arxiv.org/abs/2201.09178},
    year={2022}
}
```

## License

Seq2Pat is licensed under the [GNU GPL License 2.0](LICENSE).

<br>

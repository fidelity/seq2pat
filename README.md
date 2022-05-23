[![ci](https://github.com/fidelity/seq2pat/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/fidelity/seq2pat/actions/workflows/ci.yml) [![PyPI version fury.io](https://badge.fury.io/py/seq2pat.svg)](https://pypi.python.org/pypi/seq2pat/) [![PyPI license](https://img.shields.io/pypi/l/seq2pat.svg)](https://pypi.python.org/pypi/seq2pat/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Downloads](https://static.pepy.tech/personalized-badge/seq2pat?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/seq2pat)


Seq2Pat: Sequence-to-Pattern Generation Library
===============================================

Seq2Pat (AAAI'22) is a research library for sequence-to-pattern generation to discover
sequential patterns that occur frequently in large sequence databases.
The library supports constraint-based reasoning to specify
desired properties over patterns.

From an algorithmic perspective, the library takes advantage of
[multi-valued decision diagrams](https://www.springer.com/us/book/9783319428475).
It is based on the state-of-the-art approach for sequential pattern mining
from [Hosseininasab _et. al._ AAAI 2019](https://aaai.org/ojs/index.php/AAAI/article/view/3962).

From an implementation perspective, the library is written in ```Cython```
that brings together the efficiency of a low-level ```C++``` backend and
the expressiveness of a high-level ```Python``` public interface.

Seq2Pat is developed as a joint collaboration between Fidelity Investments
and the Tepper School of Business at CMU. Documentation is available at [fidelity.github.io/seq2pat](https://fidelity.github.io/seq2pat).

## Quick Start
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

# Run DPM to get mined patterns
aggregation_to_patterns = dichotomic_pattern_mining(seq2pat_pos, seq2pat_neg, 
                                                    min_frequency_pos=1, 
                                                    min_frequency_neg=2)

# DPM patterns with Union aggregation
dpm_patterns = aggregation_to_patterns[DichotomicAggregation.union]

# Encodings of all sequences
sequences = sequences_pos + sequences_neg
pat2feat = Pat2Feat()
encodings = pat2feat.get_features(sequences, dpm_patterns, drop_pattern_frequency=False)
```

## Available Constraints

The library offers various constraint types, including a number of non-monotone constraints.

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.
* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.
* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.
* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

## Usage Examples

Examples on how to use the available constraints can be found 
in the [Usage Example Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/usage_example.ipynb).

Supported by Seq2Pat, we proposed **Dichotomic Pattern Mining** ([X. Wang and S. Kadioglu, 2022](https://arxiv.org/abs/2201.09178)) to analyze the correlations between 
mined patterns and different outcomes of sequences. DPM plays an integrator role between Sequential 
Pattern Mining and the downstream modeling tasks, by generating embeddings of sequences based on the mined frequent patterns.
An example on how to run DPM and generate pattern embeddings can be found in 
[Dichotomic Pattern Mining Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/dichotomic_pattern_mining.ipynb).

## Installation

Seq2Pat can be installed from PyPI using ``pip install seq2pat``. It can also be installed from source by following the instructions in
our [documentation](https://fidelity.github.io/seq2pat/installation.html).

### Requirements

The library requires ```Python 3.6+```, the ```Cython``` package, and a ```C++``` compiler.
See [requirements.txt](requirements.txt) for dependencies.

## Support

Please submit bug reports, questions and feature requests as [Issues](https://github.com/fidelity/seq2pat/issues).

## Citation

If you use Seq2Pat in a publication, please cite it as:

```bibtex
  @article{seq2pat2022,
    author={Wang Xin, Hosseininasab Amin, Colunga Pablo, Kadioglu Serdar, van Hoeve Willem-Jan},
    title={Seq2Pat: Sequence-to-Pattern Generation for Constraint-based Sequential Pattern Mining},
    url={https://github.com/fidelity/textwiser},
    journal={Proceedings of the AAAI Conference on Artificial Intelligence},
    volume={TBD},
    number={TBD},
    year={2022},
    pages={TBD}
  }
```

To cite the Dichotomic Pattern Mining framework, please cite it as:

```bibtex
@inproceedings{DPM2022,
    title={Dichotomic Pattern Mining with Applications to Intent Prediction from Semi-Structured Clickstream Datasets}, 
    author={Xin Wang and Serdar Kadioglu},
    booktitle={The AAAI-22 Workshop on Knowledge Discovery from Unstructured Data in Financial Services},
    year={2022},
    eprint={2201.09178},
    archivePrefix={arXiv}
}
```

## License

Seq2Pat is licensed under the [GNU GPL License 2.0](LICENSE).

<br>

Seq2Pat: Sequence-to-Pattern Generation Library
===============================================

Seq2Pat is a research library for sequence-to-pattern generation to discover
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
and the Tepper School of Business at CMU.

## Quick Start
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

## Available Constraints

The library offers various constraint types, including a number of non-monotone constraints.

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.
* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.
* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.
* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

## Usage Examples

Examples on how to use the available constraints can be found 
in the [Jupyter Notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/usage_example.ipynb).

## Installation

Seq2Pat can be installed from PyPI using ``pip install seq2pat`` or it can be installed from source by following the instructions in
our [documentation](https://fidelity.github.io/seq2pat/installation.html).

### Requirements

The library requires ```Python 3.6+```, the ```Cython``` package, and a ```C++``` compiler.
See [requirements.txt](requirements.txt) for dependencies.

## Support

Please submit bug reports and feature requests as [Issues](https://github.com/fidelity/seq2pat/issues).

## License

Seq2Pat is licensed under the [GNU GPL License 2.0](LICENSE).

<br>

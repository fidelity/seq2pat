---
title: 'Seq2Pat: Sequence-to-Pattern Generation Library'

tags:
  - Python
  - Sequential Pattern Mining
  - Frequent Itemset Mining
  - Multi-valued Decision Diagrams

authors:
  - name: Xin Wang
    affiliation: 1
  - name: Amin Hosseininasab
    affiliation: 2
  - name: Pablo Colunga
    affiliation: 3
  - name: Serdar Kadioglu
    affiliation: 1
  - name: Willem-Jan van Hoeve
    affiliation: 2

affiliations:
  - name: AI Center of Excellence, Fidelity Investments, USA
    index: 1
  - name: Tepper School of Business, Carnegie Mellon University, USA
    index: 2
  - name: College of Computer Information Science, Northeastern University, USA
    index: 3

date: 28 April 2020
bibliography: reference.bib

---

# Summary

`Seq2Pat` is a research library for sequence-to-pattern generation to
discover sequential patterns that occur frequently in large sequence databases.
The library supports constraint-based reasoning to specify desired properties over patterns.   

# Usage Example

To present the high-level functionality, let us consider a simple example to
show how to find frequent sequential patterns from a given sequence database subject to constraints.   

```python
# Import Seq2Pat library
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

In this simple scenario,
there are three _sequences_, i.e., ordered list of items, in the given sequence database.
The sequence is associated with an _attribute_ that captures the price of every item.
There is a _constraint_ that restricts the average price of items of a pattern to be between three to four.
Finally, the _min_frequency_ condition initiates a search for patterns that occur at least in two sequences.   

Patterns ["A", "D"], ["B", "A"], and ["C", "A"] occur in two sequences.
However, only the ["A", "D"] pattern meets the average price condition.
In the first sequence, there are multiple items "A" holding different attributes, "5" and "8" respectively.
Although the attributes ["8", "2"] violates the average condition, ["5", "2"] still makes ["A", "D"] become a qualified pattern.
Another qualified ["A", "D"] pattern is from the third sequence.
Accordingly, for this sequence database with the given price attribute,
the average price constraint, and the minimum frequency condition,
`Seq2Pat` returns the pattern ["A", "D"] as the only satisfying pattern.


It is possible to extend this scenario with multiple attributes
and other constraint types such as the gap, median, and span constraints, for example, introducing a timestamp attribute to
capture frequent patterns where users spend at least a minimum duration
amount of time on certain items that have specific price ranges.    

# Background

## Sequential Pattern Mining (SPM)

In Pattern Mining literature,
a sequence database represents an _ordered_ list of items or events.
Such databases help capture relationships in various practical applications such as
a sequence of customer purchases, medical treatments, call patterns, digital click-stream activities, among others.
Given such a sequence database, Sequential Pattern Mining (SPM) aims at finding patterns of interest
that occur frequently.

## Constraint-based SPM

When all possible combinations are considered,
the number of sequential patterns in databases is huge.
Therefore, it is important to design efficient and scalable
pattern mining algorithms that can search for a set of patterns
that satisfy minimum support, referred to as _frequency_.
Not only that but in practice, finding the entire set of
frequent patterns in a database is not of great interest.
The resulting number of items is still typically too large
and fails to provide significant insight to the user.
It is hence desirable to incorporate various kinds of
problem-specific constraints that restrict the search to
smaller subsets of interesting patterns.
For example, in online retail click-stream analysis,
we may seek frequent browsing patterns from sessions
where users spend at least a minimum amount of time on certain items
that have specific price ranges.
Such constraints limit the output and are much more effective
in knowledge discovery compared to an arbitrarily large set of
frequent click-streams.
Despite their applicability, when it comes to off-the-shelf
tools, the library support for sequential pattern mining remains limited,
in particular for the Python technology stack.
`Seq2Pat` is designed and developed to fill this gap.

# Seq2Pat: Sequence-to-Pattern Generation Library

`Seq2Pat` is a research library for sequence-to-pattern generation
to find sequential patterns that occur frequently in large sequence databases.
The library supports constraint-based reasoning to specify desired properties over patterns.   

Novel techniques that leverage the multi-valued decision diagram
(MDD) [@DBLP:series/aifta/BergmanCHH16] representation of the database are introduced
in [@DBLP:conf/aaai/HosseininasabHC19]. In particular, this representation can
accommodate multiple item attributes and various constraint types.
The MDD algorithm has already been shown to be competitive with or
superior to existing sequential pattern mining algorithms in terms of
scalability and efficiency [@DBLP:conf/aaai/HosseininasabHC19].
The `Seq2Pat` library makes these efficient algorithms
accessible to a broad audience with a user-friendly interface.

# Seq2Pat: High-Level Features  

**[Algorithm]**
From an algorithmic perspective,
the library takes advantage of multi-valued decision diagrams [@DBLP:series/aifta/BergmanCHH16].
It is based on the state-of-the-art approach for sequential pattern mining from [@DBLP:conf/aaai/HosseininasabHC19].   

**[Implementation]**
From an implementation perspective,
the library is written in Cython that brings together the efficiency of
a low-level C++ backend and the expressiveness of a high-level Python public interface.   

**[Interface]**
The `Seq2Pat` API is designed to provide a class-based and user-friendly
interface to a significantly modified version of an MDD-based prefix-projection
algorithm [@MPP] written in C++.
The original implementation was re-designed to enable integration with Cython
while ensuring the reproducibility of the original results and keeping any
potential runtime or memory overhead at a minimum.

**[Dependencies]**
Other than the Cython package, `Seq2Pat` is self-contained and does not rely on
any other external library. As such, it interfaces well with the Python
technology stack and is ready to be leveraged in existing data mining pipelines.  

**[Audience]**
`Seq2Pat` is designed to be used by researchers and data science practitioners
who would like to use sequential mining algorithms in their applications with
problem-specific constraint to generate insights from sequence databases.

**[Unit Tests & Coding Standards]**
The library adheres to [PEP-8](https://www.python.org/dev/peps/pep-0008/)
style guide for Python coding standards.
It is also compliant with [numpydoc](https://numpy.org/devdocs/docs/howto_document.html)
documentation standard.
All available functionality is tested via standalone unit tests to
verify the correctness of the algorithms including invalid cases.
The source code was peer-reviewed both from a design and implementation perspective.
Operator overloading of arithmetic expressions allows introducing
pattern constraints in a natural way using numerical lower and upper bounds.
The library follows an easy-to-use API with special attention to
immutable data containers for reproducibility of results and
strict error checking for input parameters to help users avoid simple mistakes.
Publicly available methods are complete with source code documentation.
It also supports [typing](https://docs.python.org/3/library/typing.html#module-typing)
to hint argument types to the user.

**[Documentation]**
The library overview is available at
[GitHub IO pages](https://fidelity.github.io/seq2pat/quick.html)
which provides:

* Installation instructions on Windows, Linux and Mac OS.

* [Jupyter notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/usage_example.ipynb)
with usage examples for every constraint type.

* API reference guide for all the public methods.

# Seq2Pat: Available Constraints

The library offers various constraint types, including a number of anti-monotone and non-monotone constraints [@DBLP:conf/aaai/HosseininasabHC19].
To present the constraints precisely, we define a few used notations.
Let $P$ denote a sequential pattern, $\mathcal{A}$ denote the attributes of $P$ and $c$ denote a threshold.
$C_{type}(\cdot)$ is a function imposed on attributes with a certain type of operation.
The library offers the following constraints such that each type of constraint is categorized into two situations.

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.

[//]:# ($$
\max_{u-t}\{ \frac{\sum_{\alpha\in P}\alpha+\beta_1^v+\alpha^u}{|p|+\beta_2^v+1}-c\}
$$)

$$
\begin{array}{l}
C_{avg}(\mathcal{A})\le c\\
C_{avg}(\mathcal{A})\ge c
\end{array}
$$

* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.  

$$
\begin{array}{l}
C_{gap}(\mathcal{A}) \le c :=\alpha_j-\alpha_{j-1} \le c\\
\hspace{1.5cm} \alpha_j\in \mathcal{A}, 2 \le j \le |P| \\
C_{gap}(\mathcal{A})\ge c \hspace{2.65cm}
\end{array}
$$

* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.  

[//]:# (
$$
\max_{u-t}\{|\{\alpha \in u-t: \alpha\ge c\}|-|\alpha \in u-t: \alpha<c\}|\}
$$)

$$
\begin{array}{l}
C_{med}(\mathcal{A})\le c\\
C_{med}(\mathcal{A})\ge c
\end{array}
$$

* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

[//]:# ($$
\max\{\max_{\alpha\in P}\{\alpha\}, \beta_2^u\}-\min\{\min_{\alpha\in P} \{\alpha\}, \beta_1^u\}\ge c
$$)

$$
\begin{array}{l}
C_{spn}(\mathcal{A})\le c:=\max\{\mathcal{A}\}-\min\{\mathcal{A}\}\le c\\
C_{spn}(\mathcal{A})\ge c\hspace{4.12cm}
\end{array}
$$


[//]:# (TODO Add Alternatives to list a number of existing SPM algorithms, libraries, list pros/cons of the availability tools/languages, ease-of-use of our API, Attributes/Constraints etc. + add Scalability)

# References

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
	- name: College of Computer Information Science, Northeaster University, USA
	  index: 3
	  
date: 28 April 2020
bibliography: reference.bib

---

# Summary

`Seq2Pat` is a research library for sequence-to-pattern generation   
to discover sequential patterns that occur frequently in large sequence databases. 
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
there are three sequences (i.e., ordered list of items) in the sequence database. 
Each item is associated with a _price_ attribute and 
there is a constraint that restricts the _average_ price of items in a given pattern to be between three to four. 
The _min_frequency_ condition targets patterns that occur at least in two sequences.   
  
Patterns ["A", "D"], ["B", "A"], and ["C", "A"] occur in two sequences. 
However, only ["A", "D"] pattern meets the average price condition. 
Accordingly, for this sequence database with the given price attributes, 
the average price constraint and the minimum frequency condition, 
`Seq2Pat` returns the pattern ["A", "D"] as the only satisfying pattern.   
   
# Sequential Pattern Mining

In the area of Pattern Mining, 
a sequence database represents an _ordered_ list of items or events. 
Such databases help capture relationships in various practical applications such as 
sequence of customer purchases, medical treatments, call patterns, digital click-stream activity, and so on. 
Given such a database, Sequential Pattern Mining (SPM) deals with the problem of finding _interesting_ patterns 
that occur frequently.     
  
# Constraint-based SPM

When all possible combinations are considered, 
the number of sequential patterns in databases is huge. 
Therefore, it is important to design efficient and scalable 
pattern mining algorithms that can search for a set of patterns 
that satisfy a minimum support, referred to as _frequency_. 
Not only that, but in practice, finding the entire set of 
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
in knowledge discovery compared to an arbitrary large set of 
frequent click-streams.   
Despite their potential applications, when it comes to off-the-shelf 
tools, the library support remains limited, in particular for the Python technology stack.
`Seq2Pat` is built to fill this gap.

# Seq2Pat: Sequence-to-Pattern Generation Library

`Seq2Pat` is a research library for sequence-to-pattern generation 
to find sequential patterns that occur frequently in large sequence databases. 
The library supports constraint-based reasoning to specify desired properties over patterns.   

In [@DBLP:conf/aaai/HosseininasabHC19], novel techniques that leverages 
the multi-valued  decision diagram (MDD)[@DBLP:series/aifta/BergmanCHH16] 
representation of the database are introduced. 
Specifically, this representation can accommodate multiple item attributes 
and various constraint types. 
The MDD algorithm has already been shown to be competitive with or 
superior to existing sequential pattern mining algorithms in terms of 
scalability and efficiency [@DBLP:conf/aaai/HosseininasabHC19]. 
The `Seq2Pat` library makes these efficient algorithms 
accessible to a broad audience with a user-friendly interface.

# Seq2Pat: High-Level Features  
    
**[Algorithm]**
From an algorithmic perspective, 
the library takes advantage of multi-valued decision diagrams[@DBLP:series/aifta/BergmanCHH16].
It is based on the state-of-the-art approach for sequential pattern mining from [@DBLP:conf/aaai/HosseininasabHC19].   

**[Implementation]**
From an implementation perspective, 
the library is written in Cython that brings together the efficiency of 
a low-level C++ backend and the expressiveness of a high-level Python public interface.   
 
**[Interface]**
The `Seq2Pat` API is designed to provide a class-based and user-friendly 
interface to significantly modified version of fast a C++ implementation based on 
MDD-based prefix-projection algorithm[@MPP]. 
The original implementation was re-designed to enable integratation with Cython 
while ensuring the reproducibility of the original results and keeping any additional 
runtime and  memory overhead to a minimum. 
  
**[Dependencies]**
Other than the Cython package, `Seq2Pat` is self-contained and does not rely any other 
external library, hence, it interfaces well with the Python technology stack 
to be leveraged in existing data mining pipelines.  

**[Audience]**
`Seq2Pat` was designed to be used by both researchers interested in SPM algorithms 
and data science practitioners who would like to use sequential mining algorithms 
in practical applications and insight generation from sequence databases. 

**[Unit Tests & Coding Standards]**
The library adheres to [PEP-8](https://www.python.org/dev/peps/pep-0008/) 
style guide for Python coding standards. 
It is also compliant with [numpydoc ](https://numpy.org/devdocs/docs/howto_document.html) 
documentation standard. 
All available functionality is tested via standalone unit tests to 
verify the correctness of the algorithms, including the invalid cases. 
The source code under peer-review process from a design and implementation point-of-view. 
Operator overloading the arithmetic expressions allow introducing pattern constraints 
naturally with numeric lower and upper bounds. 
The library follows an easy-to-use API with special attention to 
immutable data containers for reproducibility of results and 
strict error checking for input parameters to help users avoid simple mistakes. 
Publicly available methods are complete with code documentation. 
It also supports [typing](https://docs.python.org/3/library/typing.html#module-typing) 
to hint argument types. 

**[Documentation]**
The library overview is available at 
[GitHub IO pages](https://fmr-llc.github.io/seq2pat/quick.html) 
which provides installation instructions, 
[Jupyter notebook](https://github.com/fmr-llc/seq2pat/blob/master/notebooks/usage_example.ipynb) 
with usage examples for every constraint type, and API reference guide for the public methods. 

# Seq2Pat: Available Constraints

The library offers various constraint types, 
including a number of non-monotone constraints.  
 
* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.  
 
TODO add formula 

* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.  

TODO add formula 

* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.  

TODO add formula 

* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

# Alternatives

TODO list a number of existing SPM algorithms, libraries, list pros/cons of the availability tools/languages, 
ease-of-use of our API, Attributes/Constraints etc. + add Scalability
 
# References
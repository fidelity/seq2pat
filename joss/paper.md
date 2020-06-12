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
  
To present the high-level functionality, let us consider a simple example that   
shows how to find frequent sequential patterns from a given sequence database. 

The example also highlights how constraints can introduced to specify desired properties to search for patterns of interest.  

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
# Average price constraint seq2pat.add_constraint(3 <= price.average() <= 4)   
# Patterns that occur at least twice (A-D)  
patterns = seq2pat.get_patterns(min_frequency=2)  
# >>> [“A”, “D”]
```  
  
In this scenario,  there are three _sequences_, i.e., ordered list of items, in the given sequence database.  The sequence is associated with an _attribute_ that captures the price of every item.  There is a _constraint_ that restricts the average price of items in a pattern to be between three to four.  Finally, the _min_frequency_ condition declares the search for patterns that occur at least in two sequences.     
  
Patterns ["A", "D"], ["B", "A"], and ["C", "A"] occur in two sequences.  
However, only pattern that meets the average price condition is ["A", "D"].  
In the first sequence, there are multiple occurences of item "A" reflecting different price points; "5" and "8" .  When reasoning about the ["A", "D"] pattern, even though  attributes ["8", "2"] violates the average condition, attributes ["5", "2"] still makes the patttern to satisfiy the average price condition.  
Another candidate of a qualified pattern, ["A", "D"] is found in the third sequence.  
Therefore, overall, for this sequence database with price attributes,  
the average price constraint, and the minimum frequency condition,  
`Seq2Pat` library finds and returns the pattern ["A", "D"] as the only satisfying pattern.  
  
 It is possible to extend this scenario with multiple attributes  
and other constraint types such as the **gap**, **median**, and **span** constraints. Consider, for example, introducing a timestamp attribute to  capture frequent patterns where users spend at least a minimum duration amount of time on certain items that have specific price ranges.
  
# Background  
  
## Sequential Pattern Mining (SPM)  
  
In Pattern Mining literature,  
a sequence database represents an _ordered_ list of items or events.  
Such databases help capture relationships in various practical applications such as  
sequence of customer purchases, medical treatments, call patterns, and digital click-stream activity among others. Given suchs sequence databases, Sequential Pattern Mining (SPM) aims at finding patterns that occur frequently.  
  
## Constraint-based SPM  
  
When all possible combinations are considered,  
the number of sequential patterns in databases is huge.  
Therefore, it is important to design efficient and scalable  
pattern mining algorithms that can search for a set of patterns  
that satisfy a certain threshold. This minimum support requirement 
is referred to as _frequency_.  
In practice, finding the entire set of  
frequent patterns in a database is not of great interest.  
The resulting number of items is still typically too large  
and fails to provide significant insight to the users.
What becomes important is to be able to search for patterns that are not only frequent but also exhibit certain desired properties.   
In that line of research, Constraint-based SPM incorporates 
problem-specific constraints that restrict the search to  
smaller subsets of interesting patterns.  
For example, in an online retail click-stream analysis,  
we may seek frequent browsing patterns from sessions  
where users spend at least a *minimum amount of time* on certain items  
that have *specific price ranges*.  
Such constraints help reduce the number possible set of patterns 
and are much more effective  
in knowledge discovery compared to an arbitrarily large set of  
frequent click-streams.  
Despite their applicability, when it comes to off-the-shelf  
tools, the library support for sequential pattern mining remains limited,  
in particular for the Python technology stack.  
`Seq2Pat` is designed and developed to fill this gap.  
  
# Seq2Pat: Sequence-to-Pattern Generation Library  
  
`Seq2Pat` is a research library for sequence-to-pattern generation  
to discover sequential patterns that occur frequently in large sequence databases.  
The library supports constraint-based reasoning to specify desired properties over patterns.    
  
To address the challenges of Constraint-based SPM, novel techniques that leverage the multi-valued decision diagram (MDD) [@DBLP:series/aifta/BergmanCHH16] representation of the database are introduced  
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
the library is written in $\textrm{Cython}$ that brings together the efficiency of  
a low-level $\textrm{C++}$ backend and the expressiveness of a high-level $\textrm{Python}$ public interface.     
  
**[Interface]**  
The `Seq2Pat` API is designed to provide a class-based and user-friendly  
interface to a significantly modified version of an MDD-based prefix-projection  
algorithm [@MPP] that was written in $\textrm{C++}$ originally.
The initial implementation was re-designed to enable integration with $\textrm{Cython}$
while ensuring the reproducibility of the original results and keeping any  
potential runtime or memory overhead at a minimum.  
  
**[Dependencies]**  
Other than the $\textrm{Cython} package and a $\textrm{C++}$ compiler to build the backend artifacts, `Seq2Pat` is self-contained and does not rely on  
any other external libraries. As such, it interfaces well with the Python  
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
strict error checking of input parameters to help users avoid simple mistakes.  
Publicly available methods are complete with source code documentation inluding their arguments, default parameter settings, return values, and exception cases.
The library supports [typing](https://docs.python.org/3/library/typing.html#module-typing)  
to hint argument types to the user and provide type annotation.
  
**[Documentation]**  
The library overview is available at  
[GitHub IO pages](https://fidelity.github.io/seq2pat/quick.html)  
which provides:  
  
* Installation instructions on Windows, Linux and Mac OS.  
  
* [Jupyter notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/usage_example.ipynb)  
with usage examples for every constraint type.  
  
* API reference guide for all the public methods.  

# Overview of the Approach

## Multi-Valued Decision Diagrams (MDDs)

High-level overview?

## Constraint-based SPM using MDDs

High-level overview?

# References
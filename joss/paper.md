---
title: 'Seq2Pat: Sequence-to-Pattern Generation Library'

tags:
  - Python
  - Constraint-based Sequential Pattern Mining
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

date: 04 September 2020
bibliography: reference.bib
---

# Summary

`Seq2Pat` is a research library for sequence-to-pattern generation based on Sequential Pattern Mining (SPM). The goal is to mine sequential patterns that occur frequently in large sequence databases. The library supports constraint-based SPM to specify desired properties over found patterns. 

# Sequential Pattern Mining  

A sequence database is defined as a set of _sequences_, where each sequence is an ordered set of literals or _items_. Each item may be associated to a set of _attributes_ that capture a property of the item, such as its price or quality. A _pattern_ is a subsequence of at least one sequence in the database, that maintains their original order of items. The number of sequences that contain a pattern define its _frequency_. Given such a sequence databases, SPM aims at finding patterns that occur more than a user-defined _minimum_ _frequently_.  

SPM is used in various practical applications such as mining sequence of customer purchases, medical treatments, call patterns, and digital click-stream activities, among others.         


# Constraint-based SPM  
  
In practice, finding the entire set of  frequent patterns in a database is not of great interest.  The resulting number of items is typically large and may not provide significant insight to the users. What becomes important is to be able to search for patterns that are not only frequent but also exhibit certain desired properties.   In that line of research, Constraint-based SPM incorporates problem-specific constraints that restrict the search to  smaller subsets of interesting patterns.  For example, in an online retail click-stream analysis,  we may seek frequent browsing patterns from sessions  where users spend at least a *minimum amount of time* on certain items  that have *specific price ranges*.  Such constraints help reduce the number possible set of patterns and are much more effective  in knowledge discovery compared to an arbitrarily large set of  frequent click-streams.  Despite their applicability, when it comes to off-the-shelf  tools, the library support for sequential pattern mining remains limited,  in particular for the Python technology stack.  `Seq2Pat` is designed and developed to fill this gap.    

# Statement of Need    

Despite the applicability of Sequential Pattern Mining and its potential to generate insights when combined with constraint-based reasoning, the support for available libraries and tools remain limited. The situation is even worse for the Python ecosystem which is among the most common technology stack for Machine Learning and Data Science applications. `Seq2Pat` is designed and developed to fill this gap.


# Usage Example

To present the high-level functionality, let us consider a simple example that shows how to find frequent sequential patterns from a given sequence database. 

This example also highlights how constraints can be introduced to specify desired properties in the patterns of interest.  

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
# >>> [“A”, “D”]
```  
  
In this example,  there are three sequences in the sequence database.  Items are associated with an attribute that captures the price of every item.  There is a _constraint_ that restricts the average price of items in any potential pattern to be between three and four.  Finally, the _min_frequency_ condition declares the search for patterns that occur in at least two sequences.     
  
Patterns ["A", "D"] (subsequence of sequences 1 and 3), ["B", "A"] (subsequence of sequences 1 and 2), and ["C", "A"] (subsequence of sequences 2 and 3) occur in two sequences and have a frequency of 2.  However, the only pattern that meets the average price constraint is ["A", "D"].  Note that in the first sequence, there are multiple subsequences of ["A", "D"] with different price attributes; ["5", "2"] and ["8", "2"]. The subsequence with attributes ["8", "2"] violates the average price constraint, while the subsequence with attributes ["5", "2"] satisfies the average price constraint. The average price constraint is also satisfied for the subsequence ["A", "D"] in the third sequence.  Therefore, overall, for this sequence database with a price attribute,  an average price constraint, and a minimum frequency condition of 2,  pattern ["A", "D"] is the only feasible pattern, which is found and returned by the `Seq2Pat` library.  

It is possible to extend this example with multiple attributes and other constraint types such as the **gap**, **median**, and **span** constraints. Consider, for example, introducing a timestamp attribute to  capture frequent patterns where users spend at least a minimum duration amount of time on certain items with specific price ranges.   


# Seq2Pat: Sequence-to-Pattern Generation Library  
  
`Seq2Pat` is a research library for sequence-to-pattern generation  to discover sequential patterns that occur frequently in large sequence databases.  The library supports constraint-based reasoning to specify desired properties over patterns.

To address the challenges of Constraint-based SPM, novel techniques that leverage the multi-valued decision diagram (MDD) [@DBLP:series/aifta/BergmanCHH16] representation of the database are introduced  in [@DBLP:conf/aaai/HosseininasabHC19]. In particular, this representation can  accommodate multiple item attributes and various constraint types.  The MDD algorithm has already been shown to be competitive with or  superior to existing sequential pattern mining algorithms in terms of  scalability and efficiency [@DBLP:conf/aaai/HosseininasabHC19].  The `Seq2Pat` library makes these efficient algorithms  accessible to a broad audience with a user-friendly interface.    

# Seq2Pat: High-Level Features   

Let us highlight some of the high-level features of the library. 

* **Algorithm**  
From an algorithmic perspective,  the library takes advantage of multi-valued decision diagrams [@DBLP:series/aifta/BergmanCHH16].  It is based on the state-of-the-art approach for sequential pattern mining from [@DBLP:conf/aaai/HosseininasabHC19].

  
* **Implementation**  
From an implementation perspective,  the library is written in $\textrm{Cython}$ that brings together the efficiency of  a low-level $\textrm{C++}$ backend and the expressiveness of a high-level $\textrm{Python}$ public interface.

<br> 

* **Interface**  
The `Seq2Pat` API is designed to provide a class-based and user-friendly  interface to a significantly modified version of an MDD-based prefix-projection  algorithm [@MPP] that was originally written in $\textrm{C++}$. The initial implementation was re-designed to enable integration with $\textrm{Cython}$ while ensuring the reproducibility of the original results and keeping any  potential runtime or memory overhead at a minimum. 

<br> 

* **Dependencies**  
Other than the $\textrm{Cython}$ package and a $\textrm{C++}$ compiler to build the backend artifacts, `Seq2Pat` is self-contained and does not rely on  any other external libraries. As such, it interfaces well with the Python  technology stack and is ready to be leveraged in existing data mining pipelines. 

<br> 

* **Audience**  
`Seq2Pat` is designed to be used by researchers and data science practitioners  who would like to use sequential mining algorithms in their applications with  problem-specific constraint to generate insights from sequence databases. 

<br>
 
* **Unit Tests & Coding Standards**  
The library adheres to [PEP-8](https://www.python.org/dev/peps/pep-0008/)  style guide for Python coding standards.  It is also compliant with [numpydoc](https://numpy.org/devdocs/docs/howto_document.html)  documentation standard.  All available functionality is tested via standalone unit tests to  verify the correctness of the algorithms including invalid cases.  The source code was peer-reviewed both from a design and implementation perspective.  Operator overloading of arithmetic expressions allows introducing  pattern constraints in a natural way using numerical lower and upper bounds.  The library follows an easy-to-use API with special attention to  immutable data containers for reproducibility of results and  strict error checking of input parameters to help users avoid simple mistakes.  Publicly available methods are complete with source code documentation inluding their arguments, default parameter settings, return values, and exception cases. The library supports [typing](https://docs.python.org/3/library/typing.html#module-typing)  to hint argument types to the user and provide type annotation.  

<br> 

* **Documentation**  
The library overview is available at [GitHub IO pages](https://fidelity.github.io/seq2pat/quick.html) which provides:  
  
    * Installation instructions on Windows, Linux and Mac OS.  
  
    * [Jupyter notebook](https://github.com/fidelity/seq2pat/blob/master/notebooks/usage_example.ipynb) with usage examples for every constraint type.  
  
    * API reference guide for all public methods.  
  
# Seq2Pat: Available Constraints  
  
The library offers various constraint types, including a number of anti-monotone and non-monotone constraints [@DBLP:conf/aaai/HosseininasabHC19].  To present the constraints precisely, let us define some notation. Let $P$ denote a sequential pattern, $\mathcal{A}$ denote the attributes of items in $P$, and $c$ denote a threshold.  $C_{type}(\cdot)$ is a function imposed on attributes with a certain type of operation.  The library offers the following constraints such that each type of constraint is categorized into two situations. 

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.  
  
[//]:#

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
  
[//]:#
  
$$  
\begin{array}{l}  
C_{med}(\mathcal{A})\le c\\  
C_{med}(\mathcal{A})\ge c  
\end{array}  
$$  
  
* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.  
  
[//]:#
  
$$  
\begin{array}{l}  
C_{spn}(\mathcal{A})\le c:=\max\{\mathcal{A}\}-\min\{\mathcal{A}\}\le c\\  
C_{spn}(\mathcal{A})\ge c\hspace{4.12cm}  
\end{array}  
$$  

# Seq2Pat: Algorithm Overview

## Multi-Valued Decision Diagrams

A Multi-Valued Decision diagram (MDD) is layered directed acyclic graph. MDDs have been widely used to model the feasible solution set of discrete optimization problems and as efficient data structures for sequential data [see e.g., @wegener2000branching; @DBLP:series/aifta/BergmanCHH16; @hosseininasab2019exact; @DBLP:conf/aaai/HosseininasabHC19]. Here, we use MDDs to fully encode the sequences and associated attributes of sequence databases. We refer to this data structure as the _MDD_ _database_.  

## Constraint-based SPM using MDDs

We incorporate constraints into the SPM algorithm in two steps. First, we impose certain constraints onto the MDD database by exploiting its node-arc structure. This removes infeasible patterns prior to the SPM algorithm and leads to more efficient search. Next, we generate constraint-specific information and store them at the MDD nodes. This information is used to effectively prune infeasible patterns during the mining algorithm and eliminates the need for post-processing. [@DBLP:conf/aaai/HosseininasabHC19] show that this procedure is more efficient compared to constraint-based SPM using traditional tabular encodings of the database and post processing algorithms.  

# Alternative Approaches 

Although a few python libraries exist for SPM [see e.g., @PrefixSpan-py; @pymining], to the best of our knowledge, Seq2Pat is the first Python library for constraint-based SPM. Other implementations of constraint-based SPM are mostly limited to a few constraint types, most commonly, gap, maximum span, and regular expression [see e.g. @aoga2016efficient].


# References



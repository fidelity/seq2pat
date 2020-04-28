Seq2Pat: Sequence-to-Pattern Generation Library
===============================================

Seq2Pat is a research library for sequence-to-pattern generation 
to find sequential patterns that occur frequently in large sequence databases. 
The library supports constraint-based reasoning to specify  
desired properties over patterns.  

From an algorithmic perspective, the library takes advantage of
`multi-valued decision diagrams`_.
It is based on the state-of-the-art approach for sequential pattern mining
from `Hosseininasab et. al. AAAI 2019`_.

From an implementation perspective, the library is written in ``Cython``
that brings together the efficiency of a low-level ``C++`` backend and
the expressiveness of a high-level ``Python`` public interface.

Seq2Pat is developed as a joint collaboration between Fidelity Investments 
and the Tepper School of Business at CMU. 

Available Constraints
=====================

* **Average**: This constraint specifies the average value of an attribute across all events in a pattern.

* **Gap**: This constraint specifies the difference between the attribute values of every two consecutive events in a pattern.

* **Median**: This constraint specifies the median value of an attribute across all events in a pattern.

* **Span**: This constraint specifies the difference between the maximum and the minimum value of an attribute across all events in a pattern.

.. include:: quick.rst

Source Code
===========
The source code is hosted on `GitHub`_.

.. sidebar:: Contents

   .. toctree::
    :maxdepth: 2

    quick
    installation
    examples
    api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

.. _GitHub: https://github.com/fmr-llc/seq2pat
.. _multi-valued decision diagrams: https://www.springer.com/us/book/9783319428475
.. _Hosseininasab et. al. AAAI 2019: https://aaai.org/ojs/index.php/AAAI/article/view/3962
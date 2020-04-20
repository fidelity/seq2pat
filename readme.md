Seq2Pat: Sequence-to-Pattern
========

Seq2Pat is a research library for sequence-to-pattern generation 
to find sequential patterns that occur frequently in sequence databases. 
The library supports arithmetic constraints such as 
**average**, **median**, **span**, and **gap** to 
express desired properties over patterns.  

From an algoritmic perspective, the library takes advantage of 
[multi-valued decision diagrams](https://www.springer.com/us/book/9783319428475). 
It is based on the state-of-the-art approach for sequential pattern mining
from [Hosseininasab _et. al._ AAAI'19](https://aaai.org/ojs/index.php/AAAI/article/view/3962).

From an implementation perspective, the library is written in ```Cython``` 
that brings together the efficiency of a low-level ```C++``` backend and 
the expressiveness of a high-level ```Python``` public interface.  

## Quick Start
```python
# Example to how to find sequential patterns from sequences 
from sequential.seq2pat import Seq2Pat, Attribute

# Seq2Pat over 3 sequences
seq2pat = Seq2Pat(sequences=[["A", "A", "B", "A", "D"],
                             ["C", "B", "A"],
                             ["C", "A", "C", "D"]])

# Price attribute corresponding to each event
price = Attribute(values=[[5, 5, 3, 8, 2],
                          [1, 3, 3],
                          [4, 5, 2, 1]])

# Average price constraint 
seq2pat.add_constraint(3 <= price.average() <= 4)

# Patterns that occur at least twice
patterns = seq2pat.get_patterns(min_frequency=2)
```

## Installation
The installation consists of two main steps: 
1) Build the ```C++``` backend
2) Install the ```Python``` library 

##### 1) Building the Backend
You can install the required backend artifacts from the source code using ``Cython`` 
via the ```/sequential/backend/setup.py``` script.

```python
cd seq2pat/sequential/backend
python setup.py build_ext --inplace  
```

This command will create artifacts in the ```/sequential/backend/build``` folder.
##### 2) Installing the Library

Now you can install the library on your platform from a wheel package. 

```python
cd seq2pat
pip install setuptools wheel # if wheel is not installed
python setup.py bdist_wheel
pip install dist/seq2pat-X.X.X-py3-none-any.whl
```

Don’t forget to replace ```X.X.X``` with the current version number.

---
**Requirements:**

- The library requires ``Python 3.6+``, the ``Cython`` package, 
and a ``C++`` compiler. See ```requirements.txt``` for dependencies. 

- Make sure to use the same Python version to run Seq2Pat and 
to run the ```setup.py``` script.   
 
- Make sure that the ``C++`` compiler used in your Python installation is 
the same or compatible with the ``C++`` compiler that you use to build the ```Cython``` artifacts. 
You can see the underlying ``C++`` compiler of your Python installation using ```python -i```.
 
- On Windows, you can install [MS Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
for the ```C++``` compiler. On Mac, you can install [Command Line Tools](https://developer.apple.com/)
for the ```Clang``` compiler. 

---

##### Verify Your Setup

Successful compilation creates ```Cython``` artifacts as seen 
in the directory structure below. 

To confirm that installtion was successful, run the tests included in the project.

All tests should pass.

```python
cd seq2pat
python -m unittest discover tests
```

You can now also import Seq2Pat in a Python shell or notebook.

```python
from sequential.seq2pat import Seq2Pat, Attribute
```

## Directory Structure

```
├── sequential
│
│   // Public API
│   seq2pat.py                           <- Public methods to access Seq2Pat and Attributes
│
├── backend
│
│   ├── build                            <- Build artifacts are created here
│   ├──── xxx                              
│
│   // Modified Code: No more reading from an input file and writing to an output file
│   ├── build_mdd.cpp                    <- changed. some parameter type changes. change build_mdd() signature 
│   ├── build_mdd.hpp                    <- removed reading files. change build_mdd signature
│   ├── freq_miner.cpp                   <- changed. some parameter type changes. change Freq_miner() signature
│   ├── freq_miner.hpp                   <- changed. some parameter type changes. change Freq_miner() signature
│   ├── node_mdd.cpp                     <- change function signature to pass parameters
│   ├── node_mdd.hpp                     <- change function signature to pass parameters
│   ├── pattern.hpp                      <- not changed
│
│   // Build artifacts
│   ├── seq_to_pat.cpXXX.pyd             <- Build artifact specific to python version, operating system and architecture
│   ├── seq_to_pat.cpp                   <- Build artifact
│   ├── seq_to_pat.html                  <- HTML version of seq_to_pat.pyx
│  
│   // Our Cython related code
│   ├── seq2pat.cpp                      <- Implementation of the constructor and the mining function
│   ├── seq2pat.hpp                      <- Definition of the constructor, class members, and mining function 
│   ├── seq2pat.pxd                      <- Python equivalent of hpp definition 
│   ├── seq_to_pat.pyx                   <- Python equivalent of the cpp implementation
│
│   // Installation script
│   ├── setup.py                         <- Script to compile and build the necessary artifacts 
│  
└──
```
.. _examples:

Usage Examples
==============

Examples on how to use the available constraints can be found in the `Sequential Pattern Mining Notebook`_. You can also find out how to scale up the mining capability, by running Seq2Pat on batches of sequences in parallel in `Batch Processing Notebook`_.

Supported by Seq2Pat, we proposed **Dichotomic Pattern Mining** (`X. Wang and S. Kadioglu, 2022`_) to analyze the correlations between
mined patterns and different outcomes of sequences. DPM plays an integrator role between Sequential
Pattern Mining and the downstream modeling tasks, by generating embeddings of sequences based on the mined frequent patterns.
An example on how to run DPM and generate pattern embeddings can be found in `Dichotomic Pattern Mining Notebook`_.


.. _Sequential Pattern Mining Notebook: https://github.com/fidelity/seq2pat/blob/master/notebooks/sequential_pattern_mining.ipynb
.. _X. Wang and S. Kadioglu, 2022: https://arxiv.org/abs/2201.09178
.. _Dichotomic Pattern Mining Notebook: https://github.com/fidelity/seq2pat/blob/master/notebooks/dichotomic_pattern_mining.ipynb
.. _Batch Processing Notebook: https://github.com/fidelity/seq2pat/blob/master/notebooks/batch_processing.ipynb

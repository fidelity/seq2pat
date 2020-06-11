# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0

cdef extern from "seq2pat.cpp":
    pass

from libcpp.vector cimport vector

cdef extern from "seq2pat.hpp" namespace "patterns":
    cdef cppclass Seq2pat:

        # Make sure to catch the exception, + is just a syntax
        Seq2pat() except +

        int num_att
        int N, M, L, theta          

        vector[int] lgap, ugap, lavr, uavr, lspn, uspn, lmed, umed        
        vector[int] ugapi, lgapi, uspni, lspni, uavri, lavri, umedi, lmedi   
        vector[int] num_minmax, num_avr, num_med                   
        vector[int] tot_gap, tot_spn, tot_avr                       
        vector[vector[int]] items                                   
        vector[vector[vector[int]]] attrs 
        vector[int] max_attrs, min_attrs

        # Make sure to catch the exception, + is just a syntax
        vector[vector[int]] mine() except +

# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-2.0
# distutils: language = c++

from seq2pat cimport Seq2pat
from libcpp.vector cimport vector


# seq2pat.pxd/seq_to_pat.pyx wrap seq2pat.hpp/seq2pat.cpp providing
# access to the c++ implementation of sequential
# which allows us to  build an mdd
# and mine it for frequent sequences in c++ env.
# c_seq2pat is the c++ class that we interact with directly
# through the setters and getters defined in this file.
# Parameter names and types correspond to parameter names
# and python class types that compile into c++ equalivant in
# seq2pat.cpp.
# Parameters -sequences, atttribute, constraints, etc- as
# required by build_mdd() and freq_mining() receive input
# from the _get_cython_imp(self) method in public seq2pat.py
# then each setter is called via settattr() and
# assigned to its corresponding c_seq2pat element
cdef class PySeq2pat:
    cdef Seq2pat* c_seq2pat;

    def __cinit__(self):
        # Seq2pat c++ object as defined in seq2pat.hpp/seq2pat.cpp
        self.c_seq2pat = new Seq2pat();

    def __dealloc__(self):
        del self.c_seq2pat

    def mine(self):
        return self.c_seq2pat.mine()

    @property
    def items(self):
        return self.c_seq2pat.items

    @items.setter
    def items(self, vector[vector[int]] i):
        self.c_seq2pat.items = i

    @property
    def N(self):
        return self.c_seq2pat.N

    @N.setter
    def N(self, N):
        self.c_seq2pat.N = N

    @property
    def M(self):
        return self.c_seq2pat.M

    @M.setter
    def M(self, M):
        self.c_seq2pat.M = M

    @property
    def L(self):
        return self.c_seq2pat.L

    @L.setter
    def L(self, L):
        self.c_seq2pat.L = L

    @property
    def theta(self):
        return self.c_seq2pat.theta

    @theta.setter
    def theta(self, theta):
        self.c_seq2pat.theta = theta

    @property
    def lgap(self):
        return self.c_seq2pat.lgap

    @lgap.setter
    def lgap(self, lgap):
        self.c_seq2pat.lgap = lgap

    @property
    def ugap(self):
        return self.c_seq2pat.ugap

    @ugap.setter
    def ugap(self, ugap):
        self.c_seq2pat.ugap = ugap

    @property
    def lavr(self):
        return self.c_seq2pat.lavr

    @lavr.setter
    def lavr(self, lavr):
        self.c_seq2pat.lavr = lavr

    @property
    def uavr(self):
        return self.c_seq2pat.uavr

    @uavr.setter
    def uavr(self, uavr):
        self.c_seq2pat.uavr = uavr

    @property
    def lspn(self):
        return self.c_seq2pat.lspn

    @lspn.setter
    def lspn(self, lspn):
        self.c_seq2pat.lspn = lspn

    @property
    def uspn(self):
        return self.c_seq2pat.uspn

    @uspn.setter
    def uspn(self, uspn):
        self.c_seq2pat.uspn = uspn

    @property
    def lmed(self):
        return self.c_seq2pat.lmed

    @lmed.setter
    def lmed(self, lmed):
        self.c_seq2pat.lmed = lmed

    @property
    def umed(self):
        return self.c_seq2pat.umed

    @umed.setter
    def umed(self, umed):
        self.c_seq2pat.umed = umed

    @property
    def ugapi(self):
        return self.c_seq2pat.ugapi

    @ugapi.setter
    def ugapi(self, ugapi):
        self.c_seq2pat.ugapi = ugapi

    @property
    def lgapi(self):
        return self.c_seq2pat.lgapi

    @lgapi.setter
    def lgapi(self, lgapi):
        self.c_seq2pat.lgapi = lgapi

    @property
    def uspni(self):
        return self.c_seq2pat.uspni

    @uspni.setter
    def uspni(self, uspni):
        self.c_seq2pat.uspni = uspni

    @property
    def lspni(self):
        return self.c_seq2pat.lspni

    @lspni.setter
    def lspni(self, lspni):
        self.c_seq2pat.lspni = lspni

    @property
    def uavri(self):
        return self.c_seq2pat.uavri

    @uavri.setter
    def uavri(self, uavri):
        self.c_seq2pat.uavri = uavri

    @property
    def lavri(self):
        return self.c_seq2pat.lavri

    @lavri.setter
    def lavri(self, lavri):
        self.c_seq2pat.lavri = lavri

    @property
    def umedi(self):
        return self.c_seq2pat.umedi

    @umedi.setter
    def umedi(self, umedi):
        self.c_seq2pat.umedi = umedi

    @property
    def lmedi(self):
        return self.c_seq2pat.lmedi

    @lmedi.setter
    def lmedi(self, lmedi):
        self.c_seq2pat.lmedi = lmedi

    @property
    def num_minmax(self):
        return self.c_seq2pat.num_minmax

    @num_minmax.setter
    def num_minmax(self, num_minmax):
        self.c_seq2pat.num_minmax = num_minmax

    @property
    def num_avr(self):
        return self.c_seq2pat.num_avr

    @num_avr.setter
    def num_avr(self, num_avr):
        self.c_seq2pat.num_avr = num_avr

    @property
    def num_med(self):
        return self.c_seq2pat.num_med

    @num_med.setter
    def num_med(self, num_med):
        self.c_seq2pat.num_med = num_med

    @property
    def tot_gap(self):
        return self.c_seq2pat.tot_gap

    @tot_gap.setter
    def tot_gap(self, tot_gap):
        self.c_seq2pat.tot_gap = tot_gap

    @property
    def tot_spn(self):
        return self.c_seq2pat.tot_spn

    @tot_spn.setter
    def tot_spn(self, tot_spn):
        self.c_seq2pat.tot_spn = tot_spn

    @property
    def tot_avr(self):
        return self.c_seq2pat.tot_avr

    @tot_avr.setter
    def tot_avr(self, tot_avr):
        self.c_seq2pat.tot_avr = tot_avr

    @property
    def attrs(self):
        return self.c_seq2pat.attrs

    @attrs.setter
    def attrs(self, attrs):
        self.c_seq2pat.attrs = attrs

    @property
    def max_attrs(self):
        return self.c_seq2pat.max_attrs

    @max_attrs.setter
    def max_attrs(self, max_attrs):
        self.c_seq2pat.max_attrs = max_attrs

    @property
    def min_attrs(self):
        return self.c_seq2pat.min_attrs

    @min_attrs.setter
    def min_attrs(self, min_attrs):
        self.c_seq2pat.min_attrs = min_attrs

    @property
    def num_att(self):
        return self.c_seq2pat.num_att

    @num_att.setter
    def num_att(self, num_att):
        self.c_seq2pat.num_att = num_att

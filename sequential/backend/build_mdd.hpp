// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

#pragma once

#include<vector>
#include "node_mdd.hpp"
#include "pattern.hpp"
#include "freq_miner.hpp"
#include <cmath>


void Build_MDD(vector<Node*>* datab_MDD, vector<Pattern*>* DFS_queue,
                            vector<int>* lgapi, vector<int>* ugapi, vector<int>* lspni,
                            vector<int>* uavri, vector<int>* lavri, vector<int>* umedi, vector<int>* lmedi,
                            vector<int>* lgap, vector<int>* ugap, vector<int>* lavr, vector<int>* uavr,
                            vector<int>* lspn, vector<int>* lmed, vector<int>* umed,
                            vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med, vector<int>* tot_gap,
                            vector<int>* tot_spn, vector<int>* tot_avr,
                            int M, int N, int L, int num_att, vector<int>* max_attrs,
                            vector<int>* min_attrs, vector<vector<int> >* items,
                            vector<vector<vector<int> > >* attrs);

void Disp_nodes(int, int);



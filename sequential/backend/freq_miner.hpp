// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

#pragma once

#include "pattern.hpp"
#include "node_mdd.hpp"

// Changed signature
// Returns the output
vector<vector<int>> Freq_miner(vector<Pattern*>* dfs_q, vector<int>* uspni, vector<int>* lspni, vector<int>* uavri, vector<int>* lavri, vector<int>* umedi, 
	vector<int>* lmedi, vector<int>* lavr, vector<int>* uavr, vector<int>* lspn, vector<int>* uspn, vector<int>* lmed, vector<int>* umed, 
	vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med, vector<int>* tot_spn, vector<int>* tot_avr);

void Out_final_patt(vector<int>* seq, int freq, vector<Pattern*>* dfs_q);

extern int num_patt;
extern int num_max_patt;

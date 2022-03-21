// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

#ifndef SEQ2PAT_H
#define SEQ2PAT_H

#include <vector>
#include <iostream>
#include <string>

// This class holds all the parameters
// and the method to perform mining
namespace patterns {
    class Seq2pat {
        public:

            // Parameters
            string out_file;
            int num_att;                                          
            vector<int>  lgap, ugap, lavr, uavr, lspn, uspn, lmed, umed;             
            vector<int> ugapi, lgapi, uspni, lspni, uavri, lavri, umedi, lmedi;     
            vector<int> num_minmax, num_avr, num_med;                   
            vector<int> tot_gap, tot_spn, tot_avr;
            vector<vector<int> > patterns;                       
            int N, M, L, theta;
            vector<vector<int> > items;                                    
            vector<vector<vector<int> > > attrs;
            vector<int> max_attrs, min_attrs;

            // Class object
            Seq2pat();
            ~Seq2pat();

            // Mining function
            std::vector< std::vector<int> > mine();
    };
}

#endif


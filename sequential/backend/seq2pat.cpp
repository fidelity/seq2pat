// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

#include <iostream>
#include <string.h>
#include <string>
#include "build_mdd.cpp"
#include "pattern.hpp" 
#include "freq_miner.cpp"
#include "node_mdd.cpp"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>
#include <fstream>
#include <sstream>

#include <iostream>
#include "seq2pat.hpp"

namespace patterns {

    Seq2pat::Seq2pat ()
    {
        this->num_att = 0, this->theta = 0;
    }

    Seq2pat::~Seq2pat () {}

    std::vector< std::vector<int> > Seq2pat::mine()
    {
        // This is to create a single hold of data structures as the global objects to be passed into API calls.
        // MDD database is essentially a vector of nodes
        std::vector<Node*>* datab_MDD = new vector<Node*>(M * L, NULL);
        // mdd_q is DFS queue of patterns to extend in mining algorithm
        std::vector<Pattern*>* mdd_q = new vector<Pattern*>(L, NULL);

        // results is to save mined patterns that satisfy constraints
        std::vector< std::vector<int> > results;

    	try{
    	    // Builds mdd structure in datab_MDD and create mdd_q for pattern mining algorithm
            Build_MDD(datab_MDD, mdd_q,
                      &(this->lgapi), &(this->ugapi),
                      &(this->lspni),
                      &(this->uavri), &(this->lavri), // Note that the order is other way around
                      &(this->umedi), &(this->lmedi),
                      &(this->lgap), &(this->ugap),
                      &(this->lavr), &(this->uavr),
                      &(this->lspn),
                      &(this->lmed), &(this->umed),
                      &(this->num_minmax),
                      &(this->num_avr),
                      &(this->num_med),
                      &(this->tot_gap),
                      &(this->tot_spn),
                      &(this->tot_avr),
                      this->M, this->N, this->L,
                      this->num_att, &(this->max_attrs), &(this->min_attrs),
                      &(this->items),
                      &(this->attrs));
        }
        catch(exception& e){
            throw e;
        }

        try{
            // Run frequent mining
            results = Freq_miner(mdd_q,
                                 &(this->uspni), &(this->lspni),
                                 &(this->uavri), &(this->lavri),
                                 &(this->umedi), &(this->lmedi),
                                 &(this->lavr), &(this->uavr),
                                 &(this->lspn), &(this->uspn),
                                 &(this->lmed), &(this->umed),
                                 &(this->num_minmax),
                                 &(this->num_avr),
                                 &(this->num_med),
                                 &(this->tot_spn),
                                 &(this->tot_avr),
                                 this->theta,
                                 this->L);

            // Delete MDD nodes
            for (int i=0; i < (*datab_MDD).size(); i++){
                if ((*datab_MDD)[i]!=NULL)
                    (*datab_MDD)[i]->~Node();
            }
            // Delete vectors defined in freq_miner.cpp
            std::vector<bool>().swap(indic_vec);
	        std::vector<vector<int>>().swap(result);
	        // Delete pointers
            delete datab_MDD;
            // mdd_q, the queue should be empty after calling Freq_miner() with all its patterns get popped
            delete mdd_q;

            return results;
        }
        catch(exception& e){
            throw e;
        }
    }

}

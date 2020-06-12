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
        // Queue of MDD nodes
        std::vector<Pattern*> mdd_q;

    	try{
    	    // Builds mdd structure and returns a queue of nodes
            mdd_q = Build_MDD(  &(this->lgapi), &(this->ugapi),
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
            return Freq_miner(  &mdd_q,
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
        }
        catch(exception& e){
            throw e;
        }
    }

}

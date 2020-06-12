// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

//Node function populates node with required information for constraint satisfaction. Types of information and their generation are explained in AAAI paper and not discussed here.

#include <iostream>
#include "node_mdd.hpp"
#include "build_mdd.hpp"

void Update_minmax(vector<int>& att_fnod, vector<int>& att_tnod);
void Update_sum(vector<int>& att_fnod, vector<int>& att_tnod, int att, int val, bool ub, vector<int>* num_minmax, vector<int>* num_avr);
void Update_med(vector<int>& att_fnod, vector<int>& att_tnod, int att, int val, bool ub, vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med,
	vector<int>* max_attrs, vector<int>* min_attrs);


void Node::assign_ID(int ID, int lvl, Node* tnod, vector<int>* lspni, vector<int>* lmedi, vector<int>* umedi, vector<int>* lavri, vector<int>* uavri,
	vector<int>* lavr, vector<int>* uavr, vector<int>* lmed, vector<int>* umed, 
	vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med, vector<int>* tot_spn, vector<int>* tot_avr, int num_att, 
	vector<int>* max_attrs, vector<int>* min_attrs, vector<vector<int> >* items, vector<vector<vector<int> > >* attrs) {

	if (seq_ID.empty() || seq_ID.back() != ID) {

		seq_ID.push_back(ID);
		children.push_back(new vector<Node*>);
		item = (*items)[ID - 1].at(lvl - 1);
		attr.emplace_back(new vector<vector<int>*>(num_att, NULL));
		if (!(*tot_spn).empty() || !(*tot_avr).empty() || !(*umedi).empty() || !(*lmedi).empty()){
			for (int att = 0; att < num_att; att++){
				attr.back()->at(att) = new vector<int>(1 + (*num_minmax)[att] + (*num_avr)[att] * 2 + (*num_med)[att] * 3, (*attrs)[att].at(ID - 1).at(lvl - 1));
				for (int ii = 0; ii < (*num_avr)[att]; ii++)
					attr.back()->at(att)->at(1 + (*num_minmax)[att] + (*num_avr)[att] + ii) = 1;
			}
			for (int att = 0; att < (*lmedi).size(); att++){
				if ((*attrs)[(*lmedi)[att]].at(ID - 1).at(lvl - 1) < (*lmed)[att]){
					attr.back()->at((*lmedi)[att])->at((*num_minmax)[(*lmedi)[att]] + (*num_avr)[(*lmedi)[att]] * 2 + 1) = 0;
					attr.back()->at((*lmedi)[att])->at((*num_minmax)[(*lmedi)[att]] + (*num_avr)[(*lmedi)[att]] * 2 + 3) = (*max_attrs)[(*lmedi)[att]] + 1;
				}
				else{
					attr.back()->at((*lmedi)[att])->at((*num_minmax)[(*lmedi)[att]] + (*num_avr)[(*lmedi)[att]] * 2 + 1) = 0;
					attr.back()->at((*lmedi)[att])->at((*num_minmax)[(*lmedi)[att]] + (*num_avr)[(*lmedi)[att]] * 2 + 2) = (*min_attrs)[(*lmedi)[att]] - 1;
				}
			}
			for (int att = 0; att < (*umedi).size(); att++){
				if ((*attrs)[(*umedi)[att]].at(ID - 1).at(lvl - 1) > (*umed)[att]){
					attr.back()->at((*umedi)[att])->at((*num_minmax)[(*umedi)[att]] + (*num_avr)[(*umedi)[att]] * 2 + ((*num_med)[(*umedi)[att]] - 1) * 3 + 1) = 0;
					attr.back()->at((*umedi)[att])->at((*num_minmax)[(*umedi)[att]] + (*num_avr)[(*umedi)[att]] * 2 + ((*num_med)[(*umedi)[att]] - 1) * 3 + 2) = (*min_attrs)[(*umedi)[att]] - 1;
				}
				else{
					attr.back()->at((*umedi)[att])->at((*num_minmax)[(*umedi)[att]] + (*num_avr)[(*umedi)[att]] * 2 + ((*num_med)[(*umedi)[att]] - 1) * 3 + 1) = 0;
					attr.back()->at((*umedi)[att])->at((*num_minmax)[(*umedi)[att]] + (*num_avr)[(*umedi)[att]] * 2 + ((*num_med)[(*umedi)[att]] - 1) * 3 + 3) = (*max_attrs)[(*umedi)[att]] + 1;
				}
			}

		}
	}

	if (tnod != NULL) {
		children.back()->push_back(tnod);
		
		for (vector<int>::iterator it = (*lspni).begin(); it != (*lspni).end(); it++){
			Update_minmax(*(attr.back()->at(*it)), *(tnod->attr.back()->at(*it)));
		}

		int att = 0;
		for (vector<int>::iterator it = (*uavri).begin(); it != (*uavri).end(); it++){
			Update_sum(*(attr.back()->at(*it)), *(tnod->attr.back()->at(*it)), *it, (*uavr)[att], 1, num_minmax, num_avr);
			att++;
		}

		att = 0;
		for (vector<int>::iterator it = (*lavri).begin(); it != (*lavri).end(); it++){
			Update_sum(*(attr.back()->at(*it)), *(tnod->attr.back()->at(*it)), *it, (*lavr)[att], 0, num_minmax, num_avr);
			att++;
		}

		att = 0;
		for (vector<int>::iterator it = (*umedi).begin(); it != (*umedi).end(); it++){
			Update_med(*(attr.back()->at(*it)), *(tnod->attr.back()->at(*it)), *it, (*umed)[att], 1, num_minmax, num_avr, num_med, max_attrs, min_attrs);
			att++;
		}

		att = 0;
		for (vector<int>::iterator it = (*lmedi).begin(); it != (*lmedi).end(); it++){
			Update_med(*(attr.back()->at(*it)), *(tnod->attr.back()->at(*it)), *it, (*lmed)[att], 0, num_minmax, num_avr, num_med, max_attrs, min_attrs);
			att++;
		}

	}

}

void Update_minmax(vector<int>& att_fnod, vector<int>& att_tnod){
	
	if (att_tnod[1] < att_fnod[1])
		att_fnod[1] = att_tnod[1];
	if (att_tnod[2] > att_fnod[2])
		att_fnod[2] = att_tnod[2];

}

void Update_sum(vector<int>& att_fnod, vector<int>& att_tnod, int att, int val, bool ub, vector<int>* num_minmax, vector<int>* num_avr) {

	if (ub && val * (1 + att_tnod[(*num_minmax)[att] + (*num_avr)[att] + 1]) - (att_fnod[0] + att_tnod[(*num_minmax)[att] + 1]) > val * att_fnod[(*num_minmax)[att] + (*num_avr)[att] + 1] - att_fnod[(*num_minmax)[att] + 1]){
		att_fnod[(*num_minmax)[att] + 1] = att_fnod[0] + att_tnod[(*num_minmax)[att] + 1];
		att_fnod[(*num_minmax)[att] + (*num_avr)[att] + 1] = 1 + att_tnod[(*num_minmax)[att] + (*num_avr)[att] + 1];
	}
	else if (!ub && val * (1 + att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2]) - (att_fnod[0] + att_tnod[(*num_minmax)[att] + (*num_avr)[att]]) < val * att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2] - att_fnod[(*num_minmax)[att] + (*num_avr)[att]]){
		att_fnod[(*num_minmax)[att] + (*num_avr)[att]] = att_fnod[0] + att_tnod[(*num_minmax)[att] + (*num_avr)[att]];
		att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2] = 1 + att_tnod[(*num_minmax)[att] + 2 * (*num_avr)[att]];
	}

}


void Update_med(vector<int>& att_fnod, vector<int>& att_tnod, int att, int val, bool ub, vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med,
	vector<int>* max_attrs, vector<int>* min_attrs){

	if (ub){
		int tnod1, tnod2, tnod3;
		if (att_tnod[0] <= val){
			tnod1 = 1;
			tnod2 = att_tnod[0];
			tnod3 = (*max_attrs)[att] + 1;
		}
		else{
			tnod1 = -1;
			tnod2 = (*min_attrs)[att] - 1;
			tnod3 = att_tnod[0];
		}
		if (att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1] + tnod1 > att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1]){
			att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1] = tnod1 + att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1];
			if (tnod2 > att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2])
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2] = tnod2;
			else
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2] = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2];
			if (tnod3 < att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3])
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] = tnod3;
			else
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3];
		}
		else if (att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1] + tnod1 == att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 1]){
			int fnod2, fnod3;
			if (tnod2 > att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2])
				fnod2 = tnod2;
			else
				fnod2 = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2];
			if (tnod3 < att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3])
				fnod3 = tnod3;
			else
				fnod3 = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3];


			double avrf = 0.5 * (att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] + att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2]);
			double avrt = 0.5 * (fnod3 + fnod2);
			if (avrt <= val && avrf > val){ //one sat -> keep sat
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2] = fnod2;
			}
			else if (avrt <= val && avrf <= val && fnod3 < att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3]){//both sat -> keep min of fnod3
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2] = fnod2;
			}
			else if (avrt > val && avrf > val && fnod2 < att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2]){//both sat -> keep min of fnod2
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + ((*num_med)[att] - 1) * 3 + 2] = fnod2;
			}
		}
	}	
	else {
		int tnod1, tnod2, tnod3;
		if (att_tnod[0] >= val){
			tnod1 = 1;
			tnod2 = (*min_attrs)[att] - 1;
			tnod3 = att_tnod[0];
		}
		else{
			tnod1 = -1;
			tnod2 = att_tnod[0];
			tnod3 = (*max_attrs)[att] + 1;
		}

		if (att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1] + tnod1 > att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1]){
			att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1] = tnod1 + att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1];
			if (tnod2 > att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2])
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2] = tnod2;
			else
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2] = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2];
			if (tnod3 < att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3])
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] = tnod3;
			else
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3];
		}
		else if (att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1] + tnod1 == att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 1]){
			int fnod2, fnod3;
			if (tnod2 > att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2])
				fnod2 = tnod2;
			else
				fnod2 = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2];
			if (tnod3 < att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3])
				fnod3 = tnod3;
			else
				fnod3 = att_tnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3];

			double avrf = 0.5 * (att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] + att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2]);
			double avrt = 0.5 * (fnod3 + fnod2);
			if (avrt >= val && avrf < val){ //one sat -> keep sat
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2] = fnod2;
			}
			else if (avrt >= val && avrf >= val && fnod2 > att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2]){//both sat -> keep max of fnod2
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2] = fnod2;
			}
			else if (avrt < val && avrf < val && fnod3 > att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3]){//both inf -> keep max of fnod3
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 3] = fnod3;
				att_fnod[(*num_minmax)[att] + (*num_avr)[att] * 2 + 2] = fnod2;
			}
		}
	}
}

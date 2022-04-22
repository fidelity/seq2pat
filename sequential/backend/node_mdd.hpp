// -*- coding: utf-8 -*-
// SPDX-License-Identifier: GPL-2.0

#pragma once

#include<vector>

using namespace std;

class Node {

public:

	int ID;									//Node number in graph
	int parent;								//Used to determine whether node has parent w.r.t to a Seq ID
	int item;

	vector<int> seq_ID;						//Vector which keeps the sequences associated to node
	vector<vector<vector<int>*>*> attr;		//Vector of critical information, one row per sequence, per attribute, columns: 0:actual, min:1, max:size_maxmin, min_sum:size_maxmin + 1, max_sum:size_maxmin + size_sum, num(avr):last
	vector<vector<Node*>*> children;

	void assign_ID(int ID, int lvl, Node* tnod, vector<int>* lspni, vector<int>* lmedi, vector<int>* umedi, vector<int>* lavri, vector<int>* uavri,
	vector<int>* lavr, vector<int>* uavr, vector<int>* lmed, vector<int>* umed, 
	vector<int>* num_minmax, vector<int>* num_avr, vector<int>* num_med, vector<int>* tot_spn, vector<int>* tot_avr, int num_att, 
	vector<int>* max_attrs, vector<int>* min_attrs, vector<vector<int> >* items, vector<vector<vector<int> > >* attrs);	 //Creates or updates the node information

	Node() { ID = 0; parent = 0; item = 0; }			//Node constructor

	~Node() {
		for (int i = 0; i < children.size(); i++){
			delete children[i];
		}
//		Clear the vector children and deallocate memory by swapping with an empty vector
		std::vector<vector<Node*>*>().swap(children);

		for (int i=0; i < attr.size(); i++){
		    for (int j = 0; j < attr[i]->size(); j++)
					delete attr[i]->at(j);
		    delete attr[i];
		}
		std::vector<vector<vector<int>*>*>().swap(attr);

		std::vector<int>().swap(seq_ID);
	}

};


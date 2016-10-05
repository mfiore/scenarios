/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   Clean.h
 * Author: mfiore
 *
 * Created on August 12, 2016, 11:22 AM
 */

#ifndef CLEANOBJECT_H
#define CLEANOBJECT_H

#include "Hmdp.h"

#include <string>
#include <vector>
#include "MdpBasicActions.h"

using namespace std;
class CleanObject: public Hmdp {
public:
    CleanObject(string agent_name, std::vector<std::string> locations);
    CleanObject(const CleanObject& orig);
    virtual ~CleanObject();
    
private:

    std::map<VariableSet, double> transitionFunction(VariableSet state, string action);
    int rewardFunction(VariableSet state, string action);
    bool isGoalState(VariableSet state);
    bool isStartingState(VariableSet state);
    
    string agent_loc_var_;
    string object_loc_var_;

    string agent_name_;
    string object_name_;
    string object_placement_;
    
    
    
};
#endif
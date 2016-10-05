 /* Created on August 12, 2016, 11:22 AM
 */

#ifndef GOOUT_H
#define GOOUT_H

#include "Mdp.h"

#include <string>
#include <vector>
#include "MdpBasicActions.h"
#include "ConcreteMdp.h"

using namespace std;
class GoOut: public ConcreteMdp {
public:
    GoOut(string agent_name, std::vector<std::string> locations,
        std::map<std::string,std::vector<std::string> > connections);
    GoOut(const GoOut& orig);
    virtual ~GoOut();
    
private:

    std::map<VariableSet, double> transitionFunction(VariableSet state, string action);
    int rewardFunction(VariableSet state, string action);
    bool isGoalState(VariableSet state);
    bool isStartingState(VariableSet state);
    
    string agent_loc_var_;
    string keys_loc_var_;
    
    string agent_name_;
    string keys_name_;
    string outside_name_;

    std::map<std::string,std::vector<std::string> > connections_;
};
#endif /* GOOUT_H */
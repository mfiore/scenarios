 /* Created on August 12, 2016, 11:22 AM
 */

#ifndef WATCHTV_H
#define WATCHTV_H

#include "Mdp.h"

#include <string>
#include <vector>
#include "MdpBasicActions.h"
#include "ConcreteMdp.h"

using namespace std;
class WatchTv: public ConcreteMdp {
public:
    WatchTv(string agent_name, std::vector<std::string> locations,
        std::map<std::string,std::vector<std::string> > connections);
    WatchTv(const WatchTv& orig);
    virtual ~WatchTv();
    
private:

    std::map<VariableSet, double> transitionFunction(VariableSet state, string action);
    int rewardFunction(VariableSet state, string action);
    bool isGoalState(VariableSet state);
    bool isStartingState(VariableSet state);
    
    string agent_loc_var_;
    string remote_loc_var_;
    
    string agent_name_;
    string remote_name_;
    string sofa_name_;

    std::map<std::string,std::vector<std::string> > connections_;
};
#endif /* WATCHTV_H */
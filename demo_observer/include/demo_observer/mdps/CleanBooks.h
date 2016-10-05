#ifndef CLEANBOOK_H
#define CLEANBOOK_H

#include "Mdp.h"

#include <string>
#include <vector>
#include "MdpBasicActions.h"
#include "ConcreteMdp.h"

using namespace std;
class CleanBooks: public ConcreteMdp {
public:
    CleanBooks(string agent_name, string read_location, std::vector<std::string> locations,
        std::map<std::string,std::vector<std::string> > connections);
    CleanBooks(const CleanBooks& orig);
    virtual ~CleanBooks();
    
private:

    std::map<VariableSet, double> transitionFunction(VariableSet state, string action);
    int rewardFunction(VariableSet state, string action);
    bool isGoalState(VariableSet state);
    bool isStartingState(VariableSet state);
    
    string agent_loc_var_;
    string book1_loc_var_;
    string book2_loc_var_;
    string book3_loc_var_;
    
    string agent_name_;
    string book_name_;
    string place_location_name_;

    std::map<std::string,std::vector<std::string> > connections_;
    
};
#endif /* CleanBooks_H */
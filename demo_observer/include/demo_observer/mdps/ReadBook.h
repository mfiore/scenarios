 /* Created on August 12, 2016, 11:22 AM
 */

#ifndef READBOOK_H
#define READBOOK_H

#include "Mdp.h"

#include <string>
#include <vector>
#include "MdpBasicActions.h"
#include "ConcreteMdp.h"

using namespace std;
class ReadBook: public ConcreteMdp {
public:
    ReadBook(string agent_name, string read_location, std::vector<std::string> locations,
        std::map<std::string,std::vector<std::string> > connections);
    ReadBook(const ReadBook& orig);
    virtual ~ReadBook();
    
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
    string read_location_name_;
    std::map<std::string,std::vector<std::string> > connections_;
    
    
};
#endif /* READBOOK_H */
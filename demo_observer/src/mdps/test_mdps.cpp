#include <ros/ros.h>
#include "demo_observer/mdps/DrinkSomething.h"

#include <string>
#include <vector>
#include <map>

int main(int argc, char** argv) {
	ros::init(argc,argv,"test_mdps");

	string mdp_name=argv[2];

	std::vector<std::string> locations={"table","sidetable","bathroom","outside","shelf1","shelf2","shelf3","sofa"};
	std::map<std::string,std::string> initial_state;
	initial_state["agent_isAt"]="table";
	initial_state["mug_isAt"]="sidetable";
	initial_state["waterbottle_isAt"]="shelf1";
	initial_state["teabottle_isAt"]="shelf2";
	VariableSet v_i;
	v_i.set=initial_state;


	if (mdp_name=="DrinkWater") {
		DrinkSomething drink_water("agent","mug","waterbottle",locations);
		drink_water.create("drink_water",true);

		drink_water.simulate(5,initial_state);
	}
	else if (mdp_name=="DrinkTea") {
		DrinkSomething drink_tea("agent","mug","teabottle",locations);
		drink_tea.create("drink_tea",true);
		drink_tea.simulate(5,initial_state);
	}

}
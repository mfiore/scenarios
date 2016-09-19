#include <ros/ros.h>
#include "demo_observer/mdps/DrinkSomething.h"

#include <string>
#include <vector>

int main(int argc, char** argv) {
	ros::init(argc,argv,"create_mdps");

	string mdp_name=argv[2];

	std::vector<std::string> locations={"table","sidetable","bathroom","outside","shelf1","shelf2","shelf3","sofa"};

	if (mdp_name=="DrinkWater") {
		DrinkSomething drink_water("agent","mug","waterbottle",locations);
		drink_water.create("drink_water",true);
	}
	else if (mdp_name=="DrinkTea") {
		DrinkSomething drink_tea("agent","mug","teabottle",locations);
		drink_tea.create("drink_tea",true);
	}

}
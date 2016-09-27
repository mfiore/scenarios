#include <ros/ros.h>
#include "demo_observer/mdps/DrinkSomething.h"

#include <string>
#include <vector>

int main(int argc, char** argv) {
	ros::init(argc,argv,"create_mdps");

	ROS_INFO("CREATE_MDP - started node");
	string mdp_name=argv[1];

	ROS_INFO("CREATE_MDP - mdp name is %s",mdp_name.c_str());

	std::vector<std::string> locations={"table","sidetable","bathroom","outside","shelf1","shelf2","shelf3",
	"sofa","livingroom"};

	if (mdp_name=="drink_water") {
		DrinkSomething drink_water("agent","mug","waterbottle",locations);
		drink_water.create("drink_water",true);
	}
	else if (mdp_name=="drink_tea") {
		DrinkSomething drink_tea("agent","mug","teabottle",locations);
		drink_tea.create("drink_tea",true);
	}

}
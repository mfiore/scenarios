#include <ros/ros.h>
#include "demo_observer/mdps/DrinkSomething.h"
#include "Mdp.h"
#include <string>
#include <vector>
#include <map>

int main(int argc, char** argv) {
	ros::init(argc,argv,"test_mdps");

	ROS_INFO("TEST_MDPS - started node test-mdps");

	string mdp_name=argv[1];

	ROS_INFO("TEST_MDPS - mdp name is %s",mdp_name.c_str());

	std::vector<std::string> locations = {"table", "sidetable", "bathroom", "outside", "shelf1", "shelf2", "shelf3", "sofa"};
	  std::map<std::string, std::string> initial_state;
	  initial_state["agent_isAt"] = "table";
	  initial_state["mug_isAt"] = "sidetable";
	  initial_state["waterbottle_isAt"] = "shelf1";
	  initial_state["teabottle_isAt"] = "shelf2";
	  initial_state["has_drunk"] = "0";
	  initial_state["mug_capacity"] = "0";
	  initial_state["waterbottle_capacity"] = "1";
	  VariableSet v_i;
	  v_i.set = initial_state;

	  std::map<std::string,std::string> parameter_map;
	  parameter_map["agent"]="agent";
	  
	  Mdp drink_water;
	  drink_water.readMdp("/home/mfiore/"+mdp_name);
	  drink_water.assignParameters(parameter_map);
	  drink_water.simulate(8, v_i);

}
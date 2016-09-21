#ifndef Drink_H
#define Drink_H

#include <ros/ros.h>

#include <action_nodes/Action.h>
#include <string>
#include <vector>
#include <situation_assessment_msgs/Fact.h>

class Drink: public Action {
	public:
	Drink(ros::NodeHandle node_handle);
	
protected:
	bool checkPreconditions(StringMap parameters);
	void setPostconditions(StringMap parameters);
};

#endif
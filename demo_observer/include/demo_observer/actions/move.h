#ifndef Move_H
#define Move_H

#include <ros/ros.h>

#include <action_nodes/Action.h>
#include <string>
#include <vector>
#include <situation_assessment_msgs/Fact.h>

class Move: public Action {
	public:
	Move(ros::NodeHandle node_handle);
	
protected:
	bool checkPreconditions(StringMap parameters);
	void setPostconditions(StringMap parameters);
};

#endif
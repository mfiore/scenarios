#ifndef Fill_H
#define Fill_H

#include <ros/ros.h>

#include <action_nodes/Action.h>
#include <string>
#include <vector>
#include <situation_assessment_msgs/Fact.h>

class Fill: public Action {
	public:
	Fill(ros::NodeHandle node_handle);
	
protected:
	bool checkPreconditions(StringMap parameters);
	void setPostconditions(StringMap parameters);
};

#endif
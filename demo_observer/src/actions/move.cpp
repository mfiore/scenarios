#include "demo_observer/actions/move.h"

Move::Move(ros::NodeHandle node_handle):Action("move",node_handle) {
	parameters_.push_back("target");
	parameters_.push_back("main_agent");
}

bool Move::checkPreconditions(StringMap parameters) {
	ROS_INFO("%s - checking preconditions",action_name_.c_str());
	
	if (!checkParameterPresence(parameters)) return false;

	situation_assessment_msgs::Fact query;
	query.model=robot_name_;
	query.subject=parameters.at("main_agent");
	query.predicate.push_back("at");

	string location=queryDatabase(query);

	situation_assessment_msgs::Fact connected_query;
	query.model=robot_name_;
	query.subject=location;
	query.predicate.push_back("connected");
	query.predicate.push_back(parameters.at("target"));

	bool is_connected=std::stoi((queryDatabase(query)));
	return is_connected;

}
void Move::setPostconditions(StringMap parameters) {
	// std::vector<situation_assessment_msgs::Fact> facts;

	// situation_assessment_msgs::Fact remove_f,add_f;
	// add_f.model=robot_name_;
	// add_f.subject=parameters.at("main_agent");
	// add_f.predicate.push_back("at");

	// remove_f=add_f;
	// add_f.value.push_back(parameters.at("target"));

	// remove_f.value.push_back()

}

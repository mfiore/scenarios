#include "demo_observer/actions/fill.h"

Fill::Fill(ros::NodeHandle node_handle):Action("fill",node_handle) {
	parameters_.push_back("target");
	parameters_.push_back("main_agent");
	parameters_.push_back("main_object");
}

bool Fill::checkPreconditions(StringMap parameters) {
	// ROS_INFO("%s - checking preconditions",action_name_.c_str());

	if (!checkParameterPresence(parameters)) return false;

	
	situation_assessment_msgs::Fact has_query;
	has_query.model=robot_name_;
	has_query.subject=parameters.at("main_agent");
	has_query.predicate.push_back("has");
	has_query.predicate.push_back(parameters.at("main_object"));

	bool has_object=std::stoi(queryDatabase(has_query));

	if (!has_object) return false;


	situation_assessment_msgs::Fact capacity_query;
	capacity_query.model=robot_name_;
	capacity_query.subject=parameters.at("main_object");
	capacity_query.predicate.push_back("capacity");

	int object_capacity=std::stoi(queryDatabase(capacity_query));

	if (object_capacity==0) return false;

	situation_assessment_msgs::Fact agent_isAt_query,target_isAt_query;
	agent_isAt_query.model=robot_name_;
	agent_isAt_query.subject=parameters.at("main_agent");
	agent_isAt_query.predicate.push_back("at");

	string agent_location=queryDatabase(agent_isAt_query);

	target_isAt_query=agent_isAt_query;
	target_isAt_query.subject=parameters.at("target");

	string target_location=queryDatabase(target_isAt_query);

	return agent_location==target_location;

}
void Fill::setPostconditions(StringMap parameters) {
	string target=parameters.at("target");
	string object=parameters.at("object");

	situation_assessment_msgs::Fact target_capacity,object_capacity;
	target_capacity.model=robot_name_;
	target_capacity.subject=target;
	target_capacity.predicate.push_back("capacity");
	target_capacity.value.push_back("1");

	object_capacity=target_capacity;
	object_capacity.subject=object;
	object_capacity.value.clear();
	object_capacity.value.push_back("0");

	std::vector<situation_assessment_msgs::Fact> fact_vector={target_capacity,object_capacity};
	setFacts(fact_vector);
}

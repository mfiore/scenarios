#include "demo_observer/actions/fill.h"

Fill::Fill(ros::NodeHandle node_handle):Action("fill",node_handle) {
	parameters_.push_back("target");
	parameters_.push_back("main_agent");
	parameters_.push_back("main_object");
}

bool Fill::checkPreconditions(StringMap parameters) {
	// ROS_INFO("%s - checking preconditions",action_name_.c_str());

	if (!checkParameterPresence(parameters)) return false;

	string agent=parameters.at("main_agent");
	string object=parameters.at("main_object");
	string target=parameters.at("target");

	situation_assessment_msgs::Fact object_type_query;
	object_type_query.model=robot_name_;
	object_type_query.subject=object;
	object_type_query.predicate={"type"};
	string object_type=queryDatabase(object_type_query);
	if (object_type!="bottle") return false;

	
	situation_assessment_msgs::Fact has_query;
	has_query.model=robot_name_;
	has_query.subject=agent;
	has_query.predicate.push_back("has");
	has_query.value.push_back(object);

	bool has_object=queryDatabase(has_query)!="";

	// ROS_INFO("Has object is %d",has_object);
	if (!has_object) return false;


	situation_assessment_msgs::Fact capacity_query;
	capacity_query.model=robot_name_;
	capacity_query.subject=object;
	capacity_query.predicate.push_back("capacity");

	int object_capacity=std::stoi(queryDatabase(capacity_query));

	// ROS_INFO("capacity is %d",object_capacity);
	if (object_capacity==0) return false;
	return true;
	situation_assessment_msgs::Fact agent_isAt_query,target_isAt_query;
	agent_isAt_query.model=robot_name_;
	agent_isAt_query.subject=parameters.at("main_agent");
	agent_isAt_query.predicate.push_back("isInArea");

	std::vector<std::string> agent_location=queryDatabaseComplete(agent_isAt_query);

	target_isAt_query=agent_isAt_query;
	target_isAt_query.subject=target;

	std::vector<std::string> target_location=queryDatabaseComplete(target_isAt_query);

	return agent_location==target_location;

}
void Fill::setPostconditions(StringMap parameters) {
	if (!checkParameterPresence(parameters)) {
		ROS_INFO("FILL - not all parameters are present");
		return;
	}


	string target=parameters.at("target");
	string object=parameters.at("main_object");

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

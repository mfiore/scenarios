#include <ros/ros.h>

#include "demo_observer/actions/drink.h"
#include "demo_observer/actions/fill.h"
#include "demo_observer/actions/move.h"
#include "situation_assessment_msgs/AddArea.h"


ros::ServiceClient add_area_client_;

void addArea(string name, std::vector<geometry_msgs::Point32> points) {
	situation_assessment_msgs::AddArea s;
	s.request.name=name;
	s.request.area.points=points;
	s.request.linked_to_entity="";

	if (add_area_client_.call(s)) {
		ROS_INFO("DEMO_SCENARIO - added area for %s",name.c_str());
	}
	else {
		ROS_WARN("DEMO_SCENARIO - error contacting add area service");
	}

}
geometry_msgs::Point32 createPoint(double x, double y) {
	geometry_msgs::Point32 p;
	p.x=x;
	p.y=y;
	p.z=0;
	return p;
}

int main(int argc,char **argv) {
	ros::init(argc,argv,"demo_scenario");

	ros::NodeHandle node_handle;

	Drink drink(node_handle);
	Fill fill(node_handle);
	Move move(node_handle);

	add_area_client_=node_handle.serviceClient<situation_assessment_msgs::AddArea>(
		"situation_assessment/add_area",1000);

	ROS_INFO("DEMO_SCENARIO - Connecting to add area");
	add_area_client_.waitForExistence();
	ROS_INFO("DEMO_SCENARIO - connected");

	std::vector<std::string> locations;
	double area_size;
	node_handle.getParam("demo_observer/locations",locations);
	node_handle.getParam("demo_observer/area_size",area_size);
	for (string l: locations) {
		double x,y,z;
		node_handle.getParam("simulation/starting_position/"+l+"/x",x);
		node_handle.getParam("simulation/starting_position/"+l+"/y",y);
		node_handle.getParam("simulation/starting_position/"+l+"/z",z);

		vector<geometry_msgs::Point32> points={createPoint(x-area_size,y-area_size),
			createPoint(x-area_size,y+area_size),createPoint(x+area_size,y+area_size),createPoint(x+area_size,y-area_size)};
		addArea(l,points);
	}

	ros::spin();
}
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
	ROS_INFO("DEMO_OBSERVER - starting node");

	ros::NodeHandle node_handle;

	Drink drink(node_handle);
	Fill fill(node_handle);
	// Move move(node_handle);
	// R
	ROS_INFO("DEMO_OBSERVER created actions");

	add_area_client_=node_handle.serviceClient<situation_assessment_msgs::AddArea>("situation_assessment/add_area",1000);

	ROS_INFO("DEMO_OBSERVER - Connecting to add area");
	add_area_client_.waitForExistence();
	ROS_INFO("DEMO_OBSERVER - connected");

	std::vector<std::string> locations;
	double area_size;
	node_handle.getParam("situation_assessment/locations",locations);
	node_handle.getParam("demo_observer/area_size",area_size);
	for (string l: locations) {
		if (l!="livingroom") {
			double x,y,z;
			node_handle.getParam("simulation/starting_position/"+l+"/x",x);
			node_handle.getParam("simulation/starting_position/"+l+"/y",y);
			node_handle.getParam("simulation/starting_position/"+l+"/z",z);


			vector<geometry_msgs::Point32> points;

			if (l=="table") {
				points={createPoint(x-area_size*1.5,y-area_size*1.8),
				createPoint(x-area_size*1.5,y+area_size*1.8),createPoint(x+area_size*1.5,y+area_size*1.8),createPoint(x+area_size*1.5,y-area_size*1.8)};
			}
			// else if (l=="outside") {
				// points={createPoint(x-area_size/1.8,y-area_size/1.8),
				// createPoint(x-area_size/2,y+area_size/2),createPoint(x+area_size/2,y+area_size/2),createPoint(x+area_size/2,y-area_size/2)};				
			// }
			else  {
				points={createPoint(x-area_size,y-area_size),
				createPoint(x-area_size,y+area_size),createPoint(x+area_size,y+area_size),createPoint(x+area_size,y-area_size)};
			}

			addArea(l,points);
		}
	}
	double x,y,z;
	// vector<geometry_msgs::Point32> points={createPoint(-1.5,-2.5),createPoint(-1.5,2.5),
		// createPoint(1.5,2.5),createPoint(1.5,-2.5)};
	vector<geometry_msgs::Point32> points={createPoint(-3.5,1.5),createPoint(-3.5,5.5),
		createPoint(1.5,5.5),createPoint(1.5,1.5)};
	addArea("livingroom",points);
	ROS_INFO("DEMO_OBSERVER added areas");

	ros::spin();
}
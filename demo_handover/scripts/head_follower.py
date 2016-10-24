#!/usr/bin/env python

import sys
import py
import pr2_controller_msgs.msg
import geometry_msgs.msg

def lookAt(frame_id, x, y, z):
	point_stamped=geometry_msgs.msg.PointStamped()
	point_stamped.header.frame_id=frame_id
	point_stamped.point.x=x;
	point_stamped.point.y=y;
	point_stamped.point.z=z;

	goal=pr2_controllers_msgs.msg.PointHeadGoal()
	goal.target=point
	goal.pointing_frame="high_def_frame"
    goal.pointing_axis.x = 1;
    goal.pointing_axis.y = 0;
    goal.pointing_axis.z = 0;
    goal.min_duration = ros::Duration(0.5);
    goal.max_velocity = 1.0;

    rospy.wait_for_service('/head_traj_controller/point_head_action')
    point_head_client=rospy.ServiceProxy('/head_traj_controller/point_head_action',pr2_controllers_msgs.msg.PointHeadGoal)
    look_res=point_head_client(goal)

if __name__=='main':
	rospy.init_node("head_follower")
	rospy.loginfo("HEAD_FOLLOWER started node")
	human_to_follow=rospy.get_param("/handover/human_name")
	r=rospy.Rate(3)
	while not rospy.is_shutdown:
		lookAt(human_name+"_head",0,0,0)
		r.sleep()







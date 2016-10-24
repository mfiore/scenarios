#!/usr/bin/env python


import sys
import rospy
import action_management_msgs.srv
import geometry_msgs.msg
import situation_assessment_msgs.msg
import appl.srv
from enum import Enum
import time
from observations_collector import ObservationsCollector
from robot_manip import RobotManip
from robot_movement import RobotMovement

#Parameters
global time_to_engage_
global time_to_touch_
global max_errors_


#some usefuls enums
class RobotAction(Enum):
	cont=0
	wait=1
	engage=2
	abandon=3

class RobotPose(Enum):
	extended=0
	retracted=1
	abandoned=2




global appl_started
appl_started=1


def getRobotAction(state,observations):
	rospy.wait_for_service('appl_request/handover')
	global appl_started
	try:
		get_action=rospy.ServiceProxy('appl_request/handover',appl.srv.GetAction)
		get_action_res=get_action(appl_started,observations,state)
		if appl_started==1:
			appl_started=2
		return get_action_res.action
	except rospy.ServiceException as e:
		print "Failed to call appl: "+e


def moveTo(location):
	print "moving to "+str(location)
	return True

#check if a timer has expired
def checkTimers(started_engage_timer,started_touch_timer,
				start_engage_timer,end_engage_timer,start_touch_timer,end_touch_timer):

	global time_to_engage_
	global time_to_touch_
	if (started_engage_timer and (end_engage_timer-start_engage_timer)>time_to_engage_):
		timer_engage_expired=True
	else:
		timer_engage_expired=False

	if (started_touch_timer and (end_touch_timer-start_touch_timer)>time_to_touch_):
		timer_touch_expired=True
	else:
		timer_touch_expired=False
	return (timer_engage_expired,timer_touch_expired)


def handoverLoop(observations_collector,robot_manip):

	task_completed=False #true when handover is completed
	n_timer_engage_expired=0  #the number of times the engage timer expires in a row
	started_engage_timer=False #true if the engage timer has been started
	started_touch_timer=False #true if the touch timer has been started
	start_engage_timer=0
	start_touch_timer=0
	end_engage_timer=0
	end_touch_timer=0

	global max_errors_

	#the robot start with a non extended arm and at the base
	arm_position=RobotPose.abandoned

	n_error=0 #number of motion errors
	action=None  #action to be performed by the robot from the collaborative planner

	rate=rospy.Rate(2) 

	#we quit with an abandon action
	while not rospy.is_shutdown() and action!=RobotAction.abandon:
		if robot_manip.hasReleasedGripper:
			task_completed=True

		#at the start of the loop we get the next robot's action
		if n_error<max_errors_:
			#if n_error<max we invoke the collaborative planner
			#checkTimers tests if any timer has expired
			timers=checkTimers(started_engage_timer,started_touch_timer,
				start_engage_timer,end_engage_timer,start_touch_timer,end_touch_timer)

			timer_engage_expired=timers[0]
			timer_touch_expired=timers[1]

			timer_double_expired=False #set it as false and see if we can modify it
			#if the timer engage is expired we update the maximum
			if (timer_engage_expired):
				started_engage_timer=False #reboot the timer engage
				n_timer_engage_expired=n_timer_engage_expired+1
				if n_timer_engage_expired==2:
					timer_double_expired=True
	
			if timer_touch_expired:
				started_touch_timer=False
				started_engage_timer=False
				timer_engage_expired=True
				n_timer_engage_expired=n_timer_engage_expired+1
				if n_timer_engage_expired==2:
					timer_double_expired=True

			#get state and observations in a good format for appl
			full_state=observations_collector.getFullState(task_completed,timer_engage_expired,timer_double_expired,
				timer_touch_expired)
			state=full_state[0]
			obs=full_state[1]
			#get the robot actions
			# rospy.loginfo("HANDOVER state is %s",str(state))
			# rospy.loginfo("HANDOVER obs is %s",str(obs))
			action=RobotAction(getRobotAction(state,obs))
			rospy.loginfo("HANDOVER action is %s",action)
		else:
			#if there are too many errors abandon
			action=RobotAction.abandon
			rospy.loginfo("HANDOVER max number of errors reached. Abandoning")

		if action==RobotAction.cont:
			if started_engage_timer:
				#if we were waiting and now we are not, stop the engage timer
				started_engage_timer=False 
				n_timer_engage_expired=0 #we also reboot this var and consider the event as a fresh start
			if arm_position!=RobotPose.extended:
				success=robot_manip.moveArm(RobotPose.extended.name)
				if not success:
					rospy.loginfo("HANDOVER failed to move arm to extended. Num error %d",n_error)
					n_error=n_error+1
				else:
					arm_position=RobotPose.extended
			if not started_touch_timer:
				#if the arm is extended we start a timer for the user to pick the object
				started_touch_timer=True
				start_touch_timer=time.time()

			if not robot_manip.isWaitingGripper():
				robot_manip.gripperRelease()

		elif action==RobotAction.wait:
			if started_touch_timer:
				#if we switch to wait we stop the touch timer
				started_touch_timer=False
			if arm_position==RobotPose.extended:
				robot_manip.cancelGripperRelease()
				success=robot_manip.moveArm(RobotPose.retracted.name)
				if not success:
					rospy.loginfo("HANDOVER failed to move arm to wait. Num error %d",n_error)
					n_error=n_error+1
				else:
					arm_position=RobotPose.retracted
			if not started_engage_timer:
				started_engage_timer=True
				start_engage_timer=time.time()

		elif action==RobotAction.engage:
			rospy.loginfo("HANDOVER robot is speaking")
			#toadd speech
		else:
			robot_manip.cancelGripperRelease()
			robot_manip.moveArm(RobotPose.abandoned.name)
			robot_movement.moveTo('base')

		if started_engage_timer:
			end_engage_timer=time.time()
		if started_touch_timer:
			end_touch_timer=time.time()

		rate.sleep()



def createPoint(x, y): 
	p=geometry_msgs.msg.Point32()
	p.x=x
	p.y=y
	p.z=0
	return p

def addArea(name,points):
	rospy.wait_for_service('situation_assessment/add_area')
	rospy.loginfo("HANDOVER connected to add area service")
	try:
		add_area=rospy.ServiceProxy('situation_assessment/add_area',situation_assessment_msgs.srv.AddArea)
		polygon=geometry_msgs.msg.Polygon()
		polygon.points=points
		add_area_res=add_area(name,polygon,'')
		rospy.loginfo("HANDOVER added area")
	except rospy.ServiceException as e:
		rospy.loginfo("HANDOVER failed to add area for %s",name)

def addAreas():
	points_handover=[createPoint(0.2,2.86),createPoint(-2.52,2.86),
			createPoint(-2.52,5.49),createPoint(0.2,5.49)]

	addArea("handover_location",points_handover)


if __name__ == '__main__':
	rospy.init_node("demo_handover")
	rospy.loginfo("HANDOVER started node")
	global time_to_engage_
	global time_to_touch_
	global max_errors_
	time_to_engage_=rospy.get_param("/handover/time_to_engage")
	time_to_touch_=rospy.get_param("/handover/time_to_touch")
	max_errors_=rospy.get_param("/handover/max_errors")


	rospy.loginfo("HANDOVER time to engage is %f",float(time_to_engage_))
	rospy.loginfo("HANDOVER time to touch is %f",float(time_to_touch_))
	rospy.loginfo("HANDOVER max errors is %f",float(max_errors_))

	addAreas()

	observations_collector=ObservationsCollector()
	robot_manip=RobotManip()
	robot_manip.moveArm(RobotPose.abandoned)

	robot_movement=RobotMovement()

	a=observations_collector.isHumanLocation()
	print a
	rate=rospy.Rate(2)
	while (observations_collector.isHumanLocation()=='false' and not rospy.is_shutdown()):
		rospy.loginfo("HANDOVER waiting for human")
		rate.sleep()
	if not rospy.is_shutdown():
		robot_movement.moveTo('handover_location')
		handoverLoop(observations_collector,robot_manip)
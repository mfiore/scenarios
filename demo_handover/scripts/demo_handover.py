#!/usr/bin/env python


import sys
import rospy
import action_management_msgs.srv
import appl.srv
from enum import Enum
import time

#Parameters
robot_pose_=None
robot_locations_=None
time_to_engage_=None
time_touch_=None
max_errors_=None


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

class RobotLocations(Enum):
	base=0
	exchange=1


appl_started=1



def getRobotAction(state,observations):
	rospy.wait_for_service('appl_request/handover')
	try:
		get_action=rospy.ServiceProxy('appl_request/handover',appl.srv.GetAction)
		get_action_res=get_action(appl_started,observations,state)
		return get_action_res.action
	except rospy.ServiceException as e:
		print "Failed to call appl: "+e

def moveArm(pose):

def moveTo(location):


def checkTimers():
	if (started_engage_timer and (end_engage_timer-start_engage_timer)>time_to_engage_):
		timer_engage_expired=true
		started_engage_timer=false
	else:
		timer_engage_expired=false

	if (started_touch_timer and (end_touch_timer-start_touch_timer)>time_touch_):
		timer_touch_expired=true
		started_touch_timer=false
	else:
		timer_touch_expired=false
	return (timer_engage_expired,timer_touch_expired)


def handoverLoop(observations_collector,robot_poses):

	task_completed=False #true when handover is completed
	n_timer_engage_expired=0  #the number of times the engage timer expires in a row
	started_engage_timer=False #true if the engage timer has been started
	started_touch_timer=False #true if the touch timer has been started

	#the robot start with a non extended arm and at the base
	arm_position=RobotPose.abandoned
	robot_location=RobotLocations.base

	n_error=0 #number of motion errors
	action=None  #action to be performed by the robot from the collaborative planner

	rate=rospy.Rate(2) 

	#we quit with an abandon action
	while not rospy.is_shutdown() and action!=RobotAction.abandon:
		
		#at the start of the loop we get the next robot's action
		if n_error<max_errors_:
			#if n_error<max we invoke the collaborative planner
			#checkTimers tests if any timer has expired
			timers=checkTimers(started_engage_timer,started_touch_timer,
				start_engage_timer,end_engage_timer,star_touch_timer,end_touch_timer)

			timer_engage_expired=timers[0]
			timer_touch_expired=timers[1]

			timer_double_expired=False #set it as false and see if we can modify it
			#if the timer engage is expired we update the maximum
			if (timer_engage_expired):
				started_engage_timer=False #reboot the timer engage
				n_timer_engage_expired=n_timer_engage_expired+1
				if n_timer_engage_expired==2:
					timer_double_expired=True
	

			#get state and observations in a good format for appl
			full_state=observations_collector.getFullState(task_completed,timer_engage_expired,timer_double_expired,
				touch_timer_expired)
			state=full_state[0]
			obs=full_state[1]
			#get the robot actions
			action=RobotAction(getRobotAction(state,obs))
		else:
			#if there are too many errors abandon
			action=RobotAction.abandon

		if action==RobotAction.cont:
			if started_engage_timer:
				#if we were waiting and now we are not, stop the engage timer
				started_engage_timer=False 
				n_timer_engage_expired=0 #we also reboot this var and consider the event as a fresh start
			if arm_position!=RobotPose.extended:
				success=moveArm(RobotPose.extended)
				if !success:
					rospy.logerror("HANDOVER failed to move arm to extended. Num error %d",n_error)
					n_error=n_error+1
				else
				#if the arm is extended we start a timer for the user to pick the object
					arm_position=RobotPose.extended
					started_touch_timer=True
					start_touch_timer=time.time()
			elif (started_touch_timer): 
				#we update the touch timer if the arm was already extended
				end_touch_timer=time.time()

			#elif gripper_pressure:
			#	openGripper
			#continue timer
		elif action==RobotAction.wait:
			if (started_touch_timer):
				#if we switch to wait we stop the touch timer
				started_touch_timer=False
			if arm_position==RobotPose.extended:
				#if we are moving the arm to wait we start the engage timer
				success=moveArm(RobotPose.wait)
				if !success:
					rospy.logerror("HANDOVER failed to move arm to wait. Num error %d",n_error)
					n_error=n_error+1
				else:
					arm_position=RobotPose.wait
			if !started_engage_timer:
				started_engage_timer=True
				start_engage_timer=time.time()
			else:
				#if the arm is already in wait we update the engage timer
				end_engage_timer=time.time()

		elif action==RobotAction.engage:
			#toadd speech
		else:
			moveArm(RobotPose.abandoned)
			moveTo(RobotLocations.base)

		rate.sleep()


if __name__ == '__main__':
	rospy.loginfo("HANDOVER started node")
	rospy.get_param("/handover/robot_poses",robot_poses_)
	rospy.get_param("/handover/robot_locations",robot_locations_)
	rospy.get_param("/handover/time_to_engage",time_to_engage_)
	rospy.get_param("/handover/time_touch",time_touch_)
	rospy.get_param("/handover/max_errors",max_errors_)

	moveArm(RobotPose.abandoned)

	observations_collector=ObservationsCollector()
	rate=rospy.Rate(2)
	while (not observations_collector.humanInArea()):
		rate.sleep()
	moveTo(RobotLocations.exchange)
	handoverLoop()
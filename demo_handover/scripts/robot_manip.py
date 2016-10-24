#!/usr/bin/env python

import sys
import rospy
import actionlib
import pr2motion.msg
import threading
import time

class RobotManip:
	def __init__(self):
		# Creates the SimpleActionClient, passing the type of the action
		  # (FibonacciAction) to the constructor.
		  self.client_arm = actionlib.SimpleActionClient('/pr2motion/Arm_MoveToQGoal', pr2motion.msg.Arm_Right_MoveToQGoal)

		  # Waits until the action server has started up and started
		  # listening for goals.
		  self.client_arm.wait_for_server()

		  self.client_gripper=actionlib.SimpleActionClient('/pr2motion/Gripper_Right_Operate',pr2motion.msg.Gripper_Right_Operate)

		  self.client_gripper.wait_for_server()

		  rospy.loginfo("ROBOTMANIP connected to actions for gripper and arm")

		  self.poses_list=rospy.get_param("handover/poses_list")
		  for pose in poses_list:
		  	self.poses[pose]=rospy.get_param("handover/"+pose)

		  self.is_waiting_pressure=False
		  self.has_released_gripper=False
		  self.waiting_lock=threading.Lock()
		  self.released_gripper_lock=threading.Lock()



	def moveArm(self,pose):
		if pose in self.poses_list:
			q_values=self.poses[pose]
		  	goal = pr2motion.msg.Arm_Right_MoveToQGoal(
		  		pr2motion.TRAJ_GATECH,q_values[0],q_values[1],q_values[2],
		  		q_values[3],q_values[4],q_values[5],q_values[6])
			self.client_arm.send_goal(goal)
			self.client_arm.wait_for_result()
			res=self.client_arm.get_result()
			if not res.genom_success:
				rospy.loginfo("ROBOTMANIP failed to move arm")
			return res
		else:
			rospy.loginfo("RobotManip unknown pose")
			return False

	def gripperRelease(self):
		setReleasedGripper(False)
		goal=pr2motion.msg.Gripper_Right_OperateGoal(pr2motion.GRIPPER_GRAB)
		self.client_gripper.send_goal(goal)
		setWaitingGripper(True)
		self.client_gripper.wait_for_result()
		res=self.client_gripper.get_result()
		setWaitingGripper(False)
		if res.genom_success:
			setReleasedGripper(True)



	def cancelGripperRelease(self):
		self.client_gripper.cancel_all_goals()

	def isWaitingGripper(self):
		waiting_lock.acquire()
		result=self.is_waiting_pressure
		waiting_lock.release()
		return result

	def setWaitingGripper(self,state):
		waiting_lock.acquire()
		self.is_waiting_pressure=state
		waiting_lock.release()

	def hasReleasedGripper(self):
		released_gripper_lock.acquire()
		res=self.has_released_gripper
		released_gripper_lock.release()
		return res

	def setReleasedGripper(self,state):
		released_gripper_lock.acquire()
		self.has_released_gripper=state
		released_gripper_lock.release()
		
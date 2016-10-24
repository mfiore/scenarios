#!/usr/bin/env python

import situation_assessment_msgs.srv
import situation_assessment_msgs.msg
import sys
import math
import rospy

class ObservationsCollector:


	def __init__(self):
		self.extended_distance_=rospy.get_param("/handover/extended_distance")
		self.human_name_=rospy.get_param("/handover/human_name")
		self.handover_location_=rospy.get_param("/handover/handover_location")
		self.robot_name_=rospy.get_param("/situation_assessment/robot_name")		
		
		rospy.loginfo("ObservationsCollector extended distance is %f",self.extended_distance_)
		rospy.loginfo("ObservationsCollector human name is %s",self.human_name_)
		rospy.loginfo("ObservationsCollector handover_location  is %s",self.handover_location_)
		rospy.loginfo("ObservationsCollector robot_name_ is %s",self.robot_name_)

		rospy.wait_for_service('situation_assessment/query_database')
		self.query_database_=rospy.ServiceProxy('situation_assessment/query_database',situation_assessment_msgs.srv.QueryDatabase)
		rospy.loginfo("ObservationsCollector connected to query database")


	def queryDatabase(self,fact):
		result=[]
		try:
			database_res=self.query_database_(fact)
			if len(database_res.result)>0:
				result=database_res.result[0].value
		except rospy.ServiceException as e:
			rospy.loginfo('HANDOVER error in contacting database %s',str(e))
		return result

	def isHandoverPose(self):
		fact=situation_assessment_msgs.msg.Fact()
		fact.model=str(self.robot_name_)
		fact.subject=str(self.human_name_)+"_hand"
		fact.predicate=["pose"]

		hand_pose=self.queryDatabase(fact)[0:3]

		fact.subject=self.human_name_+"_torso"

		body_pose=self.queryDatabase(fact)[0:3]

		distance=math.sqrt(

			(float(hand_pose[0])-float(body_pose[0]))**2 +
			(float(hand_pose[1])-float(body_pose[1]))**2 + 
			(float(hand_pose[2])-float(body_pose[2]))**2)
		# print distance
		# print self.extended_distance_
		return str(distance>self.extended_distance_).lower()

	def isHumanLocation(self):
		fact=situation_assessment_msgs.msg.Fact()
		fact.model=str(self.robot_name_)
		fact.subject=str(self.human_name_)+"_torso"
		fact.predicate=['isAt']

		res=self.queryDatabase(fact)
		if (len(res)>0):
			# rospy.loginfo("ObservationsCollector handover location is %s",res[0])
			return str(res[0]==self.handover_location_).lower()
		else:
			# rospy.loginfo("ObservationsCollector no response for isAt")
			return 'false'

	def isTowardRobot(self):
		fact=situation_assessment_msgs.msg.Fact()
		fact.model=str(self.robot_name_)
		fact.subject=str(self.human_name_)+"_head"
		fact.predicate=["isFacing"]

		res=self.queryDatabase(fact)
		if (len(res)>0):
			return str(res[0]==self.robot_name_).lower()
		else:
			return 'false'
			
	def getFullState(self,task_completed,timer_engage_expired,timer_double_expired,
						touch_timer_expired):
		state=str(task_completed).lower()+str(timer_engage_expired).lower()

		obs=self.isHandoverPose()+self.isHumanLocation()+str(timer_double_expired).lower()+str(touch_timer_expired).lower()+self.isTowardRobot()
		return (state,obs)





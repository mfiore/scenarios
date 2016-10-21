#!/usr/bin/env python

import situation_assessment_msgs.srv
import situation_assessment_msgs.msg
import sys
import math
import rospy

class ObservationsCollector:
	def __init__(self):
		rospy.get_param("/handover/extended_distance",extended_distance_)
		rospy.get_param("/handover/human_name",human_name_)
		rospy.get_param("/handover/handover_location",handover_location_)
		rospy.get_param("/situation_assessment/robot_name",robot_name_)

		rospy.wait_for_service('situation_assessment/query_database')
		query_database_=rospy.ServiceProxy('situation_assessment/queryDatabase',situation_assessment_msgs.srv.QueryDatabase)


	def queryDatabase(fact):
		try:
			query=situation_assessment_msgs.srv.QueryDatabase
			query.query=fact
			database_res=query_database_(query)
			if len(database_res.result)>0:
				return database_res.result[0].value
			else:
				return [None]
		except rospy.ServiceException as e:
			rospy.logerror('HANDOVER error in contacting database %s',%e)


	def isHandoverPose:
		fact=situation_assessment_msgs.msg.Fact
		fact.model=robot_name_
		fact.subject=human_name_+"_hand"
		fact.predicate.append("pose")

		hand_pose=queryDatabase(fact)[0:2]

		fact.subject=human_name_+"_body"

		body_pose=queryDatabase(fact)[0:2]

		distance=math.sqrt(
			(hand_pose[0]-body_pose[0])^2 +
			(hand_pose[1]-body_pose[1]])^2 +
			(hand_pose[2].body_pose[2])^2)
		return str(distance<extended_distance_).lower()

	def isHumanLocation():
		fact=situation_assessment_msgs.msg.Fact
		fact.model=robot_name_
		fact.subject=human_name_+"_body"
		fact.predicate.append("at")

		res=queryDatabase(fact)
		if (len(res)>0):
			return str(res[0]==handover_location_).lower()
		else:
			return 'false'

	def isTowardRobot():
		fact=situation_assessment_msgs.msg.Fact
		fact.model=robot_name_
		fact.subject=human_name_+"_body"
		fact.predicate.append("isFacing")

		res=queryDatabase(fact)
		if (len(res)>0):
			return str(res[0]==robot_name_).lower()
		else:
			return 'false'
	def getFullState(task_completed,timer_engage_expired,timer_double_expired,
						touch_timer_expired):
		state=str(task_completed).lower()+str(timer_engage_expired).lower()

		obs=isHandoverPose()+isHumanLocation()+str(timer_double_expired).lower()+str(touch_timer_expired).lower()+
		isTowardRobot()
		return (state,obs)





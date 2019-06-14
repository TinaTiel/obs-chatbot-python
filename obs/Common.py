# Contains common/shared (static) methods
import logging
from obs.Permission import Permission

log = logging.getLogger(__name__)

def eval_permission(user, required_permission):
	"""Gets the permission level of a given user and 
	checks if their permission is at least the required permission. 
	See the Permission class; MODERATOR > SUBSCRIBER > FOLLOWER > EVERYONE
	"""
	# First determine the user's permision level
	if(user['broadcaster']):
		user_permission = Permission.BROADCASTER
	elif(user['moderator']):
		user_permission = Permission.MODERATOR
	elif(user['subscriber']):
		user_permission = Permission.SUBSCRIBER
	elif(user['follower']):
		user_permission = Permission.FOLLOWER
	else:
		user_permission = Permission.EVERYONE
	
	result = user_permission >= required_permission
	log.debug("User '{}' has permission {} and required permission is {}. Operation Allowed: {}".format(user['name'], user_permission, required_permission, result))

	return result
from emission.core.wrapper.user import Tiersys
from emission.core.wrapper.user import User
import emission.core.get_database as db


def setPolarBearattr(dict):
	"""
	Sets a Polar Bear's attributes based on input dict:
		{user_id: num, username: string, happiness:int, size: int}
	"""
	polarBearCollection = db.get_polarbear_db()
	userDict = polarBearCollection.find_one({'user_id' : 'user_id'})
	if userDict == None:
		polarBearCollection.insert_one(dict)
	else:
		polarBearCollection.update_one(
			{'user_id': dict['user_id']},
			{'$set' : {'username' : dict['username'],
			'happiness' : dict['happiness'],
			'size' : dict['size']
			}}
		)

def getPolarBearattr(user_id):
	""" 
	Return a dictionary containing all Polar Bear attributes
	 {user_id: num, username: string, happiness:int, size: int}
	"""
	polarBearCollection = db.get_polarbear_db()
	return polarBearCollection.find_one({'user_id' : user_id})

def updatePolarBear(user_id):
	"""
	Updates a given uuid's associated Polar Bear
	"""
	currattr = getPolarBearattr(user_id)
	if currattr == None:
		#Create a new Polar Bear for the given user
		setPolarBearattr({'user_id': user_id,
						'username': User.getUsername(user_id),
						'happiness': User.computeHappiness(user_id),
						'size' : 0
						})
	else:
		#Update the user's Polar Bear with newer stats
		newHappiness = User.computeHappiness(user_id)
		currattr['happiness'] = newHappiness
		currattr['username'] = User.getUsername(user_id)
		#Have to user new username if user has changed it
		if newHappiness > 0.4:
			currattr['size'] += Tiersys.getUserTier(user_id)
		else:
			currattr['size'] = 0
		setPolarBearattr(currattr)


def updateAll():
	"""
	Updates all Polar Bears' attributes
	"""
	tiersys = Tiersys.getLatest()[0]['tiers']
	for tier in tiersys:
		for user_id in tier['uuids']:
			updatePolarBear(user_id)

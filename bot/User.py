class User():
	def __init__(self, username, follower=False, follower_dur=0, subscriber=False, subscriber_dur=0, moderator=False, broadcaster=False):
		self.username = username
		self.follower = follower
		self.follower_dur = follower_dur
		self.subscriber = subscriber
		self.subscriber_dur = subscriber_dur
		self.moderator = moderator
		self.broadcaster = broadcaster

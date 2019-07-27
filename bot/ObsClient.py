import obswebsocket, obswebsocket.requests
import logging

class ObsClient():
	
	def __init__(self, host='localhost', port=4444, password='', max_reconnects=3):
		self.log = logging.getLogger(__name__)
		self.host = host
		self.port = port
		self.client = obswebsocket.obsws(host, port, password)
		self.max_reconnects = max_reconnects
		if(max_reconnects <= 0):
			raise ValueError("Max reconnects must be greater than 0")

	def connect(self):
		self.log.info("Connecting to OBS Websockets on '{}' at port {}...".format(self.host, self.port))
		try:
			self.client.connect()
			self.log.info('...Connected to OBS Websockets.')
		except Exception as e:
			msg = "Could not connect to OBS! Error: {}".format(str(e))
			self.log.error(msg)
			raise Exception(msg)
	def disconnect(self):
		self.client.disconnect()

	def reconnect(self):
		self.disconnect()
		attempt = 0
		while attempt < self.max_reconnects:
			attempt += 1
			try:
				self.connect()
			except Exception as e:
				continue
			else:
				return
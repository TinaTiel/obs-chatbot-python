class ObsClient():
	
	def __init__(self, host='localhost', port=4444, password='', max_reconnects=3):
		self.host = host
		self.port = port
		self.client = obswebsocket.obsws(host, port, password)
		self.max_reconnects = max_reconnects
		if(max_reconnects <= 0):
			raise ValueError("Max reconnects must be greater than 0")

	def connect(self):
		self.client.connect()

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
import socket, sys, select, logging, time
import util

logname="logfile_client_{}.log".format(time.strftime("%y%m%d_%H%M%S"))
logging.basicConfig(
	filename=logname,
	level=logging.DEBUG,
	format='%(asctime)s %(levelname)s\t%(thread)d %(threadName)s\t%(module)s.%(funcName)s\t%(message)s')

class Client():
	"""
	"""

	def __init__(self, server_ip='localhost', server_port=9999):
		self.server_ip = server_ip
		self.server_port = server_port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		logging.debug('Client class created.')

	def connect(self):
		self.sock.connect((self.server_ip, self.server_port))
		logging.debug('Client conencted to server.')

	def close(self):
		self.sock.close()
		self.sock = None
		logging.debug('Client closed.')

	def send(self, message):
		"""
		Sends the 'message' to all in clinets in 'recipients'. If 'recipients' is either an empty list or None, then the 'message' is sent to all clients.

		'message' MUST be a byte object.
		"""
		util.send_msg(self.sock, message)
		
	def recv(self):
		"""
		Will first check if there is any data to receive in socket, if not it will
		return an empty byte object, otherwise it will return the message received.
		"""

		# Solution taken from https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
		ready = select.select([self.sock], [], [], 1)
		if ready[0]:
			logging.debug('Client received some data.')
			return util.recv_msg(self.sock)
		logging.debug('Client received no data.')
		return b''

	def info(self):
		pass

if __name__ == '__main__':
	user_input = ''
	flag = True
	c = None
	c = Client(server_port=9000)
	c.connect()
	while flag == True:
		user_input = input(" >>> ")
		if user_input == "send":
			msg = input("Message > ")
			c.send(bytes(msg, 'utf-8'))
		elif user_input == "recv":
			print("recv: {}".format(str(c.recv(), 'utf-8')))
		elif user_input == "close":
			c.close()
		elif user_input == "end":
			flag = False
		else:
			print("commands:\n send, recv, close, and end.")
	c.close()
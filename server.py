import socket
import pickle
from threading import Thread
import constants

class Server:

	def __init__(self, constants):

	# - - - - - - - - - - - - - - - - -Data structures for storing information - - - - - - - - - - - - - ---------
	
		# for storing the name of all the clients
		self.Client_list = constants.Client_list

		# {'client1':PORT}
		self.Client_ip_port = constants.Client_ip_port  

		# {'client_username':password}
		self.Client_id_pwd = constants.Client_id_pwd 

		# {'client1':socket}
		# self.UserSocket = constants.UserSocket  

		# {"Group1":[], }
		self.UsersInGroup = constants.UsersInGroup

		# {"User1":[],}
		self.GroupsOfAUser = constants.GroupsOfAUser 

		#[Group1, Group2]
		self.Group_List = constants.Group_List

		self.server_dump()

	# - - - - - - - - - -- - - - - - -- - -chat start -- - - - - - - - - - - - - - -- - - - #
	def rcv_msgs(self, client, username):
		while True:
			msg_rcvd = client.recv(2048).decode()
			self.server_load()
			if "fileusersend" in msg_rcvd.lower():   
				PEER_NAME = msg_rcvd.split(" ")[1]
				PEER_PORT = str(self.Client_ip_port[PEER_NAME])
				msg_send = PEER_NAME+":"+PEER_PORT
				client.send(bytes(msg_send, 'utf-8'))

			elif "filegroupsend" in msg_rcvd.lower():
				GRP_NAME = msg_rcvd.split(" ")[1]
				portlist = ""
				for user in self.UsersInGroup[GRP_NAME]:
					if user != username:
						portnum = self.Client_ip_port[user]
						if portlist == "":
							portlist = str(portnum) + ","+ str(user)
						else:
							portlist = portlist+":"+str(portnum)+","+ str(user)
				# print(portlist)
				client.send(bytes(portlist, 'utf-8'))

			elif "grpsend" in msg_rcvd.lower():          
				GRP_NAME = msg_rcvd.split(" ")[1]
				portlist = ""
				for user in self.UsersInGroup[GRP_NAME]:
					if user != username:
						portnum = self.Client_ip_port[user]
						if portlist == "":
							portlist = str(portnum) + ","+ str(user)
						else:
							portlist = portlist+":"+str(portnum)+","+ str(user)
				# print(portlist)
				client.send(bytes(portlist, 'utf-8'))

			elif "create" in msg_rcvd.lower():         
				GRP_NAME = msg_rcvd.split(" ")[1]
				if GRP_NAME not in self.Group_List:
					self.Group_List.append(GRP_NAME)
					self.UsersInGroup[GRP_NAME] = []
					msg_send = "Group Creation Successful"
				else:
					msg_send = "Group already exist"
				client.send(bytes(msg_send, 'utf-8'))

			elif "join" in msg_rcvd.lower():           
				GRP_NAME = msg_rcvd.split(" ")[1]
				if GRP_NAME in self.Group_List:
					if username in self.UsersInGroup[GRP_NAME]:
						msg_send = username+" already in "+GRP_NAME
					else:
						self.UsersInGroup[GRP_NAME].append(username)
						msg_send = username+" added to "+GRP_NAME
				else:
					self.UsersInGroup[GRP_NAME] = [username]
					if username in self.GroupsOfAUser.keys():
						self.GroupsOfAUser[username].append(GRP_NAME)
					else:
						self.GroupsOfAUser[username] = [GRP_NAME]
					self.Group_List.append(GRP_NAME)
					msg_send = GRP_NAME+" created succesfully and "+username+" joined successfully."
				client.send(bytes(msg_send, 'utf-8'))

			elif "send" in msg_rcvd.lower():        
				PEER_NAME = msg_rcvd.split(" ")[1]
				PEER_PORT = str(self.Client_ip_port[PEER_NAME])
				msg_send = PEER_NAME+":"+PEER_PORT
				client.send(bytes(msg_send, 'utf-8'))
			
			elif "listgrp" in msg_rcvd.lower():     
				# print ("list group")
				msg_send =""
				for key in self.UsersInGroup:
					groupName = key 
					noOfUsers = len(self.UsersInGroup[groupName])
					users = self.UsersInGroup[groupName]
					msg_send += str(groupName) +"\n"+"No of Users - "+str(noOfUsers)+"\n"
					for user in users:
						msg_send += str(user)+","
					msg_send= msg_send[:-1]	+"\n"
				if msg_send == "":
					msg_send = "No groups\n"
				client.send(bytes(msg_send, 'utf-8'))

			self.server_dump()

	# - - - - - - - - - - - - - - - - - Signup and login for client - - - - - - - - - - - - - ----
	def details_fetch(self, client):
		client.send(bytes('Please enter your username and password - ', 'utf-8'))
		user_response = client.recv(1024).decode("utf-8")
		try:
			user_response = user_response.split(" ")
			username = user_response[0]
			pwd = user_response[1]
			port = user_response[2]
			return username, pwd, port
		except:
			return 0, 0, 0

	def client_signup_login(self, client, addr):
		client.send(bytes('Press 1 for SignUp and 2 for SignIn', 'utf-8'))
		user_response = client.recv(8).decode("utf-8")

		# if True:
		try:
			self.server_load()
			if int(user_response) == 1:
				username, pwd, port = self.details_fetch(client)
				if username not in self.Client_list:
					self.Client_list.append(username)
					self.Client_id_pwd[username] = pwd
					client.send(bytes('SignUp Successful...', 'utf-8'))
					self.server_dump()
					CLIENT_THREAD = Thread(target=self.client_signup_login, args=(client, addr,))
					CLIENT_THREAD.start()
				else:
					client.send(bytes('SignUp not complete... Username already exist...', 'utf-8'))
					CLIENT_THREAD = Thread(target=self.client_signup_login, args=(client, addr,))
					CLIENT_THREAD.start()

			elif int(user_response) == 2:
				username, pwd, port = self.details_fetch(client)
				if username in self.Client_id_pwd.keys() and self.Client_id_pwd[username] == pwd:
					client.send(bytes('SignIn Successful...', 'utf-8'))
					# self.UserSocket[username] = client
					self.Client_ip_port[username] = port
					self.server_dump()
					RCV_THREAD = Thread(target=self.rcv_msgs, args=(client, username,))
					RCV_THREAD.start()
				else:
					client.send(bytes('Wrong Username or password', 'utf-8'))
					CLIENT_THREAD = Thread(target=self.client_signup_login, args=(client, addr,))  
					CLIENT_THREAD.start()

			self.server_dump()

		# else:
		except:
			CLIENT_THREAD = Thread(target=self.client_signup_login, args=(client, addr,))
			CLIENT_THREAD.start()
	
	# - - - - - - - - - - - - - - - - - Starting Server - - - - - - - - - - - - - - #
	def waiting_for_conn(self):    
		while True:
			client, addr = server.accept()

			encode_message = bytes('Connection Established', 'utf-8')
			client.send(encode_message)
			
			CLIENT_THREAD = Thread(target=self.client_signup_login, args=(client, addr,))
			CLIENT_THREAD.start()

	def server_dump(self):

		PIK = "pickle.dat"
		data = []
		data.append(self.Client_list)  
		data.append(self.Client_ip_port)  
		data.append(self.Client_id_pwd)
		# data.append(bytes(self.UserSocket))
		# for i in self.UserSocket.items():
		# 	print (type(i))
		# 	break
		data.append(self.UsersInGroup)  
		data.append(self.GroupsOfAUser)  
		data.append(self.Group_List)  
		# print ("dumping")
		# print (data)
		with open(PIK, "wb") as f:
			pickle.dump(data, f)

	def server_load(self):

		PIK = "pickle.dat"
		data = []
		with open(PIK, "rb") as f:
			data = pickle.load(f)
		# print ("data loaded")
		# print (data)
		self.Client_list = data[0]
		self.Client_ip_port = data[1]
		self.Client_id_pwd = data[2]
		# self.UserSocket = data[3]
		# print (self.UserSocket)
		self.UsersInGroup = data[3]
		self.GroupsOfAUser = data[4]
		self.Group_List = data[5]




if __name__ == "__main__":     

	MYPORT = int(input("Please assign a port number to this server - "))
	MYIP = socket.gethostname()
	MY_ADDR = (MYIP, MYPORT)     
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(MY_ADDR)
	server.listen(10)
	print("Hey, I am waiting for connections")
	server_new = Server(constants) 
	Create_conn_thread = Thread(target=server_new.waiting_for_conn)
	Create_conn_thread.start()
	Create_conn_thread.join()        

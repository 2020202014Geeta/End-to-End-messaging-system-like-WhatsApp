import socket
from threading import Thread
import math
import random 
from hashlib import sha256
from pyDes import *


class Client:
	# - - - - - - - - - - - - - - - - -Data structures for storing information - - - - - - - - - - - - - - #

	def __init__(self):            #DONE

		self.MYPORT = 1111
		self.MYIP = socket.gethostname()
		self.MY_ADDR = (MYIP, MYPORT)
		self.username = "alpha"
		self.pwd = "beta"
		self.G = 174657925435224939675987965147035581892
		self.P = 307662152597849524039519709992560403259
		# G = 2
		# test_string = "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF" 
		# P = int(test_string, 16)
		# nonce = random.randint(10**24,2**128)
		# privatekey = (str)(nonce+(int)(2020202014))
		# privatekey = '307662152597849524039519709992560403259'
		self.privatekey = str(random.randint(self.P - 1000, self.P) + 2020202014) #RANDOM NUMBER + ROLL NUMBER 
		self.privatekey = sha256((self.privatekey.encode()))
		self.privatekey = int(self.privatekey.hexdigest(), 16)        
		self.x = int(pow(self.G,self.privatekey,self.P))
		
	def key(self, receiverkey):      #DONE
		print("Secret Key", pow(receiverkey, self.privatekey, self.P))
		
	def encrypt(self, message, receiverkey):
		''' ENCRYPT THE MESSAGE USING KEY'''
		initial_value_bits = "\0\0\0\0\0\0\0\0"
		shared_secret_key = pow(receiverkey, self.privatekey, self.P)
		shared_secret_key = shared_secret_key.to_bytes(24, byteorder='little')
		k = triple_des(shared_secret_key, CBC, initial_value_bits, pad=None, padmode=PAD_PKCS5)
		encrypted_message = k.encrypt(message)          #???
		return encrypted_message

	def decrypt(self, encryptedMessage, senderkey):
		'''DECRYPT THE MESSAGE USING KEY'''
		initial_value_bits = "\0\0\0\0\0\0\0\0"
		shared_secret_key = pow(senderkey, self.privatekey, self.P)
		shared_secret_key = shared_secret_key.to_bytes(24, byteorder='little')
		k = triple_des(shared_secret_key, CBC, initial_value_bits, pad=None, padmode=PAD_PKCS5)
		decrypted_message = k.decrypt(encryptedMessage, padmode=PAD_PKCS5)
		return decrypted_message

	def peer_send(self, peer, msg_send, flag): #DONE

		if flag == 0:
			peer.send(msg_send)
		if flag == 1:
			peer.sendall(msg_send)
		return peer

	def send_msg(self):               #DONE
		while True:
			flag = 0
			msg = input()
			parsed = msg.strip().split()

			if len(parsed) > 2:
				parsed = msg.split(" ", maxsplit=2)
				if parsed[0].lower() == "fileusersend":             #DONE
					msg_send = "fileusersend "+parsed[1]
					tracker_conn.send(bytes(msg_send, "utf-8"))
					msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
					PEER_PORT = int(msg_rcvd.split(":")[1])
					PEER_IP = MYIP
					# if True:
					try:
						filePath = parsed[2]
						fileName = parsed[2].split("/")[-1]
						file = open(filePath, "rb")     #opens the file in binary format for reading
						fileContent = file.read()
						file.close()
						peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						peer.connect((PEER_IP, PEER_PORT))
						if (type)(self.x) is not bytes:
							self.x = self.x.to_bytes(24, byteorder='little')
						peer.send(self.x)
						y = peer.recv(1024)
						y = int.from_bytes(y, byteorder='little')
						
						msg = self.encrypt('fileName:'+fileName, y)
						peer.send(msg)
						peer.sendall(fileContent) #sendall is a high-level Python-only method that sends the entire buffer you pass or throws an exception. It does that by calling socket. send until everything has been sent or an error occurs.
						peer.close()
						print("FILE SENT SUCCESSFULLY TO :"+str(msg_rcvd.split(":")[0]))
					# else:
					except:
						print("FILE NOT SENT")

				elif parsed[0].lower() == "filegroupsend":       #DONE
					msg_send = "filegroupsend "+parsed[1]
					tracker_conn.send(bytes(msg_send, "utf-8"))
					msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
					list1 = msg_rcvd.split(":")
					# if True:
					try:
						filePath = parsed[2]
						fileName = parsed[2].split("/")[-1]
						file = open(filePath, "rb")
						fileContent = file.read()
						file.close()
					# else:
					except:
						print("FILE CAN'T OPEN")
					for data in list1:
						PEER_PORT = int(data.split(",")[0])
						PEER_IP = MYIP
						# if True:
						try:
							peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							peer.connect((PEER_IP, PEER_PORT))
							if (type)(self.x) is not bytes:
								self.x = self.x.to_bytes(24, byteorder='little')
							peer.send(self.x)
							y = peer.recv(1024)
							y = int.from_bytes(y, byteorder='little')						
							msg = self.encrypt('fileName:'+fileName, y)
							peer.send(msg)
							peer.sendall(fileContent)
							peer.close()
							print("FILE SENT SUCCESSFULLY TO :"+str(data.split(",")[1]))
						# else:
						except:
							print("FILE NOT SENT")

				elif parsed[0].lower() == "send":       #DONE
					msg_send = "send "+parsed[1]
					tracker_conn.send(bytes(msg_send, "utf-8"))
					msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
					# PEER_NAME = msg_rcvd.split(":")[0]
					PEER_PORT = int(msg_rcvd.split(":")[1])
					msg_send = "<"+username+"> "+parsed[2]
					print("<YOU>"+parsed[2])
					PEER_IP = MYIP
					peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					peer.connect((PEER_IP, PEER_PORT))
					if (type)(self.x) is not bytes:
						self.x = self.x.to_bytes(24, byteorder='little')
					peer.send(self.x)
					y = peer.recv(1024)
					y = int.from_bytes(y, byteorder='little')
					#ENCRYPT
					msg_encrypt = self.encrypt(msg_send, y)
					peer = self.peer_send(peer, msg_encrypt, flag)
					peer.close()

				elif parsed[0].lower() == "grpsend": #DONE
					msg_send = "grpsend "+parsed[1]
					tracker_conn.send(bytes(msg_send, "utf-8"))
					msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
					list1 = msg_rcvd.split(":")
					print("<"+parsed[1]+">"+"<YOU>"+parsed[2])       #??
					# print(list1)
					
					for data in list1:
						PEER_PORT = int(data.split(",")[0])
						PEER_IP = MYIP
						peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)					
						peer.connect((PEER_IP, PEER_PORT))
						if (type)(self.x) is not bytes:
							self.x = self.x.to_bytes(24, byteorder='little')
						peer.send(self.x)
						y = peer.recv(1024)
						y = int.from_bytes(y, byteorder='little')
						msg_send = "<"+parsed[1]+">"+"<"+username+"> "+parsed[2]
						msg_encrypt = self.encrypt(msg_send,y)
						
						peer = self.peer_send(peer, msg_encrypt, flag)
						peer.close()

			elif len(parsed) == 2:
				tracker_conn.send(bytes(msg, "utf-8"))
				msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
				print(msg_rcvd)

			elif len(parsed) == 1:       #????
				tracker_conn.send(bytes(parsed[0], "utf-8"))
				msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
				msg_rcvd = msg_rcvd[:-1]
				print(msg_rcvd)

	def chat_start(self, username, MYPORT, MYIP):      #DONE
		Rcvd_msg = Thread(target=self.client_as_server, args=(MYPORT, MYIP))
		Rcvd_msg.start()
		Send_msg = Thread(target=self.send_msg, args=())
		Send_msg.start()

	def wait_for_messages(self, peer_server):          #DONE
		while True:
			client, _ = peer_server.accept()
			y = client.recv(1024)
			y = int.from_bytes(y, byteorder='little')
			if (type)(self.x) is not bytes:
				self.x = self.x.to_bytes(24, byteorder='little')
			client.send(self.x)
			msg = client.recv(1024)
			#DECRYPT
			msg = self.decrypt(msg, y).decode("utf-8")
			if 'fileName' in msg:
				try:
					fileName = msg.split(":")[1]
					newfileName = fileName.split(".")[0] + "_copied" + "."+fileName.split(".")[-1]
					fileData = client.recv(1024)
					with open(newfileName, "wb") as F:
						while fileData:
							F.write(fileData)
							fileData = client.recv(1024)
						F.close()
					print("FILE RECEIVED SUCCESSFULLY AS:",newfileName)        # WHY IS SERVER RECIEVING A FILE
				except:
					pass
			else:
				print(msg)

	def client_as_server(self, MYPORT, MYIP):     #DONE
		# print("hello server2")
		peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		peer_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		MY_ADDR = (MYIP, MYPORT)
		peer_server.bind(MY_ADDR)
		peer_server.listen(2)
		ACCEPT_THREAD = Thread(target=self.wait_for_messages, args=(peer_server,))
		ACCEPT_THREAD.start()
		ACCEPT_THREAD.join()                #WHY JOIN USED HERE

	def login(self, username, pwd):  # WHY CONNECTION WITH THE TRACKER TWICE??
		# Tracker will ask for signin and signup
		msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
		print(msg_rcvd)
		msg_send = input()
		tracker_conn.send(bytes(msg_send, "utf-8"))
		msg_rcvd = tracker_conn.recv(1024).decode(
			"utf-8")  # Tracker will ask for username pwd
		print(msg_rcvd)
		username = input("Enter Username: ")
		pwd = input("Enter Password: ")
		msg_send = username+" "+pwd+" "+str(MYPORT)
		tracker_conn.send(bytes(msg_send, "utf-8"))  # username pwd sent to tracker
		msg_rcvd = tracker_conn.recv(1024).decode(
			"utf-8")  # Tracker will ask for username pwd
		print(msg_rcvd)
		if "SignIn Successful" in msg_rcvd:
			return True, username, pwd
		else:
			return False, username, pwd

	def printCommand(self): #DONE
		print("LIST OF COMMANDS")
		print("Send a message to User: SEND <USERNAME> <MESSAGE>")
		print("Send a message to Group: GRPSEND <GROUPNAME> <MESSAGE>")
		print("Create Group: CREATE <GROUPNAME>")
		print("Join Group: JOIN <GROUPNAME>")
		print("Send a multimedia Message to User: FILEUSERSEND <USERNAME> <FILEPATH>")
		print("Send a multimedia Message to Group: FILEGROUPSEND <GROUPNAME> <FILEPATH>")
		print("Prints list of all the Group: LISTGRP")

if __name__ == "__main__":

	MYPORT = int(input("Please assign a port number to this client - "))
	MYIP = socket.gethostname()
	TRACKERPORT = int(input("Please provide port number of the tracker - "))
	TRACERIP = socket.gethostname()
	TRACKER_ADDR = (TRACERIP, TRACKERPORT)

	tracker_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tracker_conn.connect(TRACKER_ADDR)
	# Tracker will send "Connection Established"
	msg_rcvd = tracker_conn.recv(1024).decode("utf-8")
	print(msg_rcvd)

	client_signed_in = False
	client_new = Client()	
	while client_signed_in != True:
		client_signed_in, username, pwd = client_new.login(client_new.username, client_new.pwd)
	# print("hello server2")
	client_new.printCommand()
	client_new.chat_start(username, MYPORT, MYIP)

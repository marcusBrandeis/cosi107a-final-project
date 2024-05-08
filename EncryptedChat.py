# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:13:27 2024

@author: hoski

Description: Create encrypted chat between two users. Much of this code was taken from references [4, 5] of my slideshow. Namely, NeuralNine's
             video on coding an encrypted chat log in Python, and Geeksforgeeks.org's implementation of a simple GUI chat log. My main technical
             accomplishment here was simply merging these two, and adding the ability to turn on or off various encryption algorithms, and
             adding a variable Caesar Cipher.
"""

import socket
import threading
import rsa

from tkinter import *
from tkinter import font
from tkinter import ttk


# Select which cipher to use. Please only choose one
RSA = True
Caesar = False
N = 8 # Caesar cipher number












if RSA:
    pub_key, priv_key = rsa.newkeys(1024) # your keys
    pub_key_part = None # public key of the partner


choice = input("Do you want to host (1) or to connect(2): ")

if choice == "1":
    myIP = input("Please type the IP address from which you would like to host: ")
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((myIP, 9999)) # first input is my IPv4 from command prompt, found by typing ipconfig. That is, I'm hosting on MY IP address
    
    
    server.listen()
    
    client, _ = server.accept()
    
    if RSA:
        client.send(pub_key.save_pkcs1("PEM"))
        
        pub_key_part = rsa.PublicKey.load_pkcs1(client.recv(1024))
        
        
        
        
elif choice == "2":
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    theirIP = input("Please the IP address to which you would like to connect (they must already be hosting): ")
    
    
    client.connect((theirIP, 9999)) # I'm using my IP address to host here. In general, I may want to put my own IP address, if this weren't all on the same machine. Could just do IP = input sort of thing
    
    if RSA:
        pub_key_part = rsa.PublicKey.load_pkcs1(client.recv(1024))
        
        client.send(pub_key.save_pkcs1("PEM"))
else:
    exit() # invalid input
    
    
"""
def sendMessage(client):
    # Description: How to send a message
    # client: The device running this script
    while True:
        
        message = input("")
        
        if RSA: # the encryption algorithm is RSA
            client.send(rsa.encrypt(message.encode(), pub_part))
        
        if Caesar: # the encryption algorithm is a Caesar Cipher
            message = caesarCipher(message, N)
            client.send(message.encode())
        
        else: # There is no encryption algorithm
            client.send(message.encode())
        
        print("You: ")

    
def recvMessage(client):
    # Description: How to receive a message
    # client: The device running this script
    
    
    while True:
        
        if RSA: # the encryption algorithm is RSA
            print("Partner: " + rsa.decrypt(client.recv(1024), priv_key).decode())
            
        if Caesar: # the encryption algorithm is a Caesar Cipher
            message = invCaesarCipher(client.recv(1024).decode(), N)
            print("Partner: " + message)
        
        else: # There is no encryption algorithm
            print("Partner: " + client.recv(1024).decode())
"""
    

def caesarCipher(message, N=13):
    # Takes a message and returns the same message, rotating each letter by N
    s = list(message)
    L = len(s)
    for i in range(L):
            c_i = ord(s[i])
            if (c_i >= 65) and (c_i<=90):
                    s[i] = chr((c_i-65 + N)%26 + 65)
            elif (c_i >= 97) and (c_i<= 122):
                    s[i] = chr((c_i-97 + N)%26 + 97)
    
    return "".join(s)

def invCaesarCipher(message, N = 13):
    # Takes a message and returns the same message, rotating each letter by -N
    s = list(message)
    M = 26-N
    L = len(s)
    for i in range(L):
            c_i = ord(s[i])
            if (c_i >= 65) and (c_i<=90):
                    s[i] = chr((c_i-65 + M)%26 + 65)
            elif (c_i >= 97) and (c_i<= 122):
                    s[i] = chr((c_i-97 + M)%26 + 97)
    
    return "".join(s)



# GUI class for the chat
class GUI:
	# constructor method
	def __init__(self):

		# chat window which is currently hidden
		self.Window = Tk()
		self.Window.withdraw()

		# login window
		self.login = Toplevel()
		# set the title
		self.login.title("Login")
		self.login.resizable(width=False,
							height=False)
		self.login.configure(width=400,
							height=300)
		# create a Label
		self.pls = Label(self.login,
						text="Please login to continue",
						justify=CENTER,
						font="Helvetica 14 bold")

		self.pls.place(relheight=0.15,
					relx=0.2,
					rely=0.07)
		# create a Label
		self.labelName = Label(self.login,
							text="Name: ",
							font="Helvetica 12")

		self.labelName.place(relheight=0.2,
							relx=0.1,
							rely=0.2)

		# create a entry box for
		# typing the message
		self.entryName = Entry(self.login,
							font="Helvetica 14")

		self.entryName.place(relwidth=0.4,
							relheight=0.12,
							relx=0.35,
							rely=0.2)

		# set the focus of the cursor
		self.entryName.focus()

		# create a Continue Button
		# along with action
		self.go = Button(self.login,
						text="CONTINUE",
						font="Helvetica 14 bold",
						command=lambda: self.goAhead(self.entryName.get()))

		self.go.place(relx=0.4,
					rely=0.55)
		self.Window.mainloop()

	def goAhead(self, name):
		self.login.destroy()
		self.layout(name)

		# the thread to receive messages
		rcv = threading.Thread(target=self.recvMessage)
		rcv.start()

	# The main layout of the chat
	def layout(self, name):

		self.name = name
		# to show chat window
		self.Window.deiconify()
		self.Window.title("Private Connection")
		self.Window.resizable(width=False,
							height=False)
		self.Window.configure(width=470,
							height=550,
							bg="#17202A")
		self.labelHead = Label(self.Window,
							bg="#17202A",
							fg="#EAECEE",
							text=self.name,
							font="Helvetica 13 bold",
							pady=5)

		self.labelHead.place(relwidth=1)
		self.line = Label(self.Window,
						width=450,
						bg="#ABB2B9")

		self.line.place(relwidth=1,
						rely=0.07,
						relheight=0.012)

		self.textCons = Text(self.Window,
							width=20,
							height=2,
							bg="#17202A",
							fg="#EAECEE",
							font="Helvetica 14",
							padx=5,
							pady=5)

		self.textCons.place(relheight=0.745,
							relwidth=1,
							rely=0.08)

		self.labelBottom = Label(self.Window,
								bg="#ABB2B9",
								height=80)

		self.labelBottom.place(relwidth=1,
							rely=0.825)

		self.entryMsg = Entry(self.labelBottom,
							bg="#2C3E50",
							fg="#EAECEE",
							font="Helvetica 13")

		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth=0.74,
							relheight=0.06,
							rely=0.008,
							relx=0.011)

		self.entryMsg.focus()

		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text="Send",
								font="Helvetica 10 bold",
								width=20,
								bg="#ABB2B9",
								command=lambda: self.sendButton(self.entryMsg.get()))

		self.buttonMsg.place(relx=0.77,
							rely=0.008,
							relheight=0.06,
							relwidth=0.22)

		self.textCons.config(cursor="arrow")

		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)

		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight=1,
						relx=0.974)

		scrollbar.config(command=self.textCons.yview)

		self.textCons.config(state=DISABLED)

	# function to basically start the thread for sending messages
	def sendButton(self, msg):
		self.textCons.config(state=DISABLED)
		self.msg = msg
		self.entryMsg.delete(0, END)
		snd = threading.Thread(target=self.sendMessage)
		snd.start()

	# function to receive messages
	def recvMessage(self):
		while True:
			try:
                
				if RSA: # the encryption algorithm is RSA
					message = rsa.decrypt(client.recv(1024), priv_key).decode()
                    
				elif Caesar: # the encryption algorithm is a Caesar Cipher
					message = invCaesarCipher(client.recv(1024).decode(), N)
                
				else:
					message = client.recv(1024).decode()
                    

				# if the messages from the server is NAME send the client's name
				if message == 'NAME':
					client.send(self.name.encode())
				else:
					
					# insert messages to text box
					self.textCons.config(state=NORMAL)
					self.textCons.insert(END,
										message+"\n\n")

					self.textCons.config(state=DISABLED)
					self.textCons.see(END)
                    
			except:
				# an error will be printed on the command line or console if there's an error
				print("An error occurred!")
				client.close()
				break

	# function to send messages
	def sendMessage(self):
		self.textCons.config(state=DISABLED)
		while True:
			message = (f"{self.name}: {self.msg}")
            
			
            # insert messages to text box
			self.textCons.config(state=NORMAL)
			self.textCons.insert(END, message+"\n\n")
            
			self.textCons.config(state=DISABLED)
			self.textCons.see(END)
			
            
			if RSA: # the encryption algorithm is RSA
				client.send(rsa.encrypt(message.encode(), pub_key_part))
            
			elif Caesar: # the encryption algorithm is a Caesar Cipher
				message = caesarCipher(message, N)
            
				client.send(message.encode())
			else:
				client.send(message.encode())
            
			break


# create a GUI class object
g = GUI()
    
    

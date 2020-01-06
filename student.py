import os
import platform
import mysql.connector
import MySQLdb
import re


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="mydatabase"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("SHOW DATABASES")
reg = '(0/19)?[7-9][0-9]{9}'
def Len(v):
	if(re.search(reg, v) and len(v)==10):
		return True
	else:
		return False	
	
regex = '[^@]+@[^@]+\.[^@]+'
def Check(vin):
	if(re.search(regex, vin)):
		return True
	else:
		return False
	
def manageStudent(): #Function For The Student Management System

	x = "#" * 30
	y = "=" * 28
	global bye #Making Bye As Super Global Variable
	bye = "\n {}\n# {} #\n# =======> Logged out <======= #\n# {} #\n {}".format(x, y, y, x) # Will Print GoodBye Message

	#Printing Welcome Message And options For This Program
	print(""" 

  ------------------------------------------------------
 |======================================================| 
 |======== Welcome To Student Management System	========|
 |======================================================|
  ------------------------------------------------------

	Enter 1 : To View Student's List 
	Enter 2 : To Add New Student 
	Enter 3 : To Search Student 
	Enter 4 : To Remove Student 
	Enter 5 : To sort Data
	Enter 6 : To Update
		
		""")

	try: #Using Exceptions For Validation
		userInput = int(input("Please Select An Above Option: ")) #Will Take Input From User
	except ValueError:
		exit("\nHy! That's Not A Number") #Error Message
	else:
		print("\n") #Print New Line

	#Checking Using Option	
	if(userInput == 1): #This Option Will Print List Of Students
		mycursor.execute("(SELECT count(1) FROM student)")
		if mycursor.fetchone()[0]:
			print("List Students\n") 
			
			mycursor.execute("SELECT * FROM student")
			vin = mycursor.fetchall()
			i=1
			print("SN\tRoll no.\tName\t\tAddress\t\tPhone\t\tGmail\n")				
			for a, b, c, d, e in vin:
				print("{}\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(i, a, b, c, d, e))
				i=i+1
		else:
			print("Database is epmty!\n") 

	elif(userInput == 2): #This Option Will Add New Student In The List
		print("Enter new student:\n")
		StdRollno = None
		while StdRollno is None:
			try:
				StdRollno = int(input("Enter Roll no: "))
			except ValueError:
				print("Enter Valid roll no.")		

		#Checking exixtance
		mycursor.execute("(SELECT count(1) FROM student WHERE rollno = %(rollno)s )",{'rollno':StdRollno})
		
		if mycursor.fetchone()[0]:
			print("\nThis Student {} Already In The Database".format(StdRollno))
		else: 
			StdName = input("Enter Name: ")
			StdAdd = input("Enter Address: ")
			StdPhone = ''
			while Len(StdPhone) == False:
				try:
					StdPhone = input("Enter phone no: ")
				except ValueError:
					print("Enter Valid phone no.")
			StdGmail = ''
			while Check(StdGmail) == False:
				try:
					StdGmail = input("Enter gmail no: ")
				except ValueError:
					print("Enter Valid gmail.")
			mycursor.execute("INSERT INTO student (rollno, name, address, phone, gmail) VALUES (%(rollno)s, %(name)s, %(address)s, %(phone)s, %(gmail)s)", {'rollno':StdRollno, 'name':StdName, 'address':StdAdd, 'phone':StdPhone, 'gmail':StdGmail})
			mydb.commit() #Save data on databse
			
			mycursor.execute("SELECT * FROM student")
			vin = mycursor.fetchall()
			i=1
			print("SN\tRoll no.\tName\t\tAddress\t\tPhone\t\tGmail\n")				
			for a, b, c, d, e in vin:
				print("{}\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(i, a, b, c, d, e))
				i=i+1
			print("\n New Student {} Successfully Added \n".format(StdRollno))	
			
		

	elif(userInput == 3): #This Option Will Search Student From The List
		srcStd = input("Enter Student Name To Search: ")
		mycursor.execute("(SELECT count(1) FROM student WHERE name = %(name)s )",{'name':srcStd})
	
		if mycursor.fetchone()[0]:
			print("\nRecord Found Of Student {}".format(srcStd))
		else:
			print("\nNo Record Found Of Student {}".format(srcStd)) #Error Message

	elif(userInput == 4): #This Option Will Remove Student From The List
		rmStd = input("Enter Student Name To Remove: ")
		
		mycursor.execute("(SELECT count(1) FROM student WHERE rollno = %(rollno)s )",{'rollno':rmStd})
		
		if mycursor.fetchone()[0]:
			mycursor.execute("DELETE FROM student WHERE rollno = %(rollno)s",{'rollno':rmStd})
			mydb.commit()
			print("\nStudent {} Successfully Deleted from Database \n".format(rmStd))
		else:
			print("\nNo Record Found of This Student {}".format(rmStd)) #Error Message
			
	elif(userInput == 5):
			print("\tBy Roll No \n\tEnter 0 : By Ascending.\n \tEnter non 0 : By Descending")
			userA = None
			while(userA is None):
				try: #Using Exceptions For Validation
					userA = int(input("\nPlease Select An Above Option: ")) #Will Take Input From User
				except ValueError:
					print("\nHy! That's Not A Number") #Error Message
			
			if userA == 0:
				para1='ASC'
			else:
				para1='DESC'
				
			print("\n\tBy Name \n\tEnter 0 : By Ascending.\n \tEnter non 0 : By Descending")
			userB = None
			while(userB is None):
				try: #Using Exceptions For Validation
					userB = int(input("\nPlease Select An Above Option: ")) #Will Take Input From User
				except ValueError:
					print("\nHy! That's Not A Number") #Error Message
			
			if userB == 0:
				para2='ASC'
			else:
				para2='DESC'	
				
			mycursor.execute("SELECT * FROM student ORDER BY rollno %s, name %s" %(para1, para2))			
			vin = mycursor.fetchall()
			i=1
			print("SN\tRoll no.\tName\t\tAddress\t\tPhone\t\tGmail\n")				
			for a, b, c, d, e in vin:
				print("{}\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(i, a, b, c, d, e))
				i=i+1	
			
	elif(userInput == 6):
		mycursor.execute("(SELECT count(1) FROM student)")
		if mycursor.fetchone()[0]:
			UpStd = None
			while UpStd is None:
				try:
					UpStd = int(input("Enter roll no to Update: "))
				except ValueError:
					print("Enter Valid roll no.")
			mycursor.execute("(SELECT count(1) FROM student WHERE rollno = %(roll)s )",{'roll':UpStd})
			if mycursor.fetchone()[0]:
				UpStdName = input("Enter Name: ")
				UpStdAdd = input("Enter Address: ")
				UpStdPhone = ''
				while Len(UpStdPhone) == False:
					try:
						UpStdPhone = input("Enter phone no: ")
					except ValueError:
						print("Enter Valid phone no.")
				UpStdGmail = ''
				while Check(UpStdGmail) == False:
					try:
						UpStdGmail = input("Enter gmail no: ")
					except ValueError:
						print("Enter Valid gmail.")
				mycursor.execute("UPDATE student SET name = %(name)s, address = %(address)s, phone = %(phone)s, gmail = %(gamil)s WHERE rollno = %(roll)s",{'name':UpStdName,'address':UpStdAdd,'phone':UpStdPhone,'gamil':UpStdGmail,'roll':UpStd})	
				mydb.commit()
				print("\nStudent {} Updated successfully.".format(UpStd))
			else:
				print("\nNo Record Found Of Student {}".format(UpStd)) #Error Message
			
		else:
			print("Database is epmty!\n")
		
		
	
	elif(userInput < 1 or userInput > 6): #Validating User Option
		print("Please Enter Valid Option")	#Error Message
						
manageStudent()

def runAgain(): #Making Runable Problem1353
	runAgn = input("\nwant To Run Again Y/N: ")
	if(runAgn.lower() == 'y'):
		if(platform.system() == "Windows"): #Checking User OS For Clearing The Screen
			print(os.system('cls'))
		else:
			print(os.system('clear'))
		manageStudent()
		runAgain()
	else:
		quit(bye) #Print GoodBye Message And Exit The Program

runAgain()		
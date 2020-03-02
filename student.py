import os
import platform
import mysql.connector
import MySQLdb
import re
import getpass
import string
import random

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="vinu"
)

mycursor = mydb.cursor()
#mycursor.execute("CREATE DATABASE mydatabase")
#mycursor.execute("SHOW DATABASES")
reg = '(0/19)?[7-9][0-9]{9}'

#global info
Dept_for_course=None
Course_for_student=None
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
def AddCourse():
	CName=''
	f=True
	while f==True :
		CName=input("Enter Course Name: ")
		mycursor.execute(("SELECT count(*) FROM course where CourseName=%(cname)s"),{'cname':CName})
		
		if mycursor.fetchone()[0]:
			print("Already exits please Enter different: ")
		else:
			#f=False
			#print("Already exits please Enter different: ")
			CDept=input("Enter Course Department: ")
			mycursor.execute(("SELECT count(*) FROM department where DeptName=%(cname)s"),{'cname':CDept})
			if mycursor.fetchone()[0]:	
				pass
			else:
				ask=input("Do you want to add department? ")
				if ask.lower()=='y':
					AddDept()
					
			CId=input("Enter Course ID: ")
			CFee=input("Enter fee: ")
			CDuration=input("Duration of course: ")
			Dept_for_course=CDept
			mycursor.execute(("INSERT INTO course VALUES(%(cname)s, %(cid)s, %(cfee)s, %(cduration)s, %(Cdept)s ) "),{'cname':CName,'cid':CId,'cfee':CFee,'cduration':CDuration, 'Cdept':Dept_for_course})
			mydb.commit()
			Dept_for_course=None
			
			print("New Course Added successfully!")
			f=False
			
		
def AddDept():
	DName=''
	f=True
	while f==True :
		DName=input("Enter Department Name: ")
		mycursor.execute(("SELECT count(*) FROM department where DeptName=%(dname)s"),{'dname':DName})
		
		if mycursor.fetchone()[0]:
			print("Already exits please Enter different: ")
		else:
			f=False
				
	DCode=input("Enter Department Code: ")
	DHOD=input("Enter Department HOD: ")
	DEmp=input("Enter No of employees: ")
	
	mycursor.execute(("INSERT INTO department VALUES(%(dname)s, %(dcode)s, %(dhod)s, %(demp)s ) "),{'dname':DName,'dcode':DCode,'dhod':DHOD,'demp':DEmp})
	mydb.commit()
	Dept_for_course=DName
	print("New department {} Added successfully!".format(DName))
			

def DelStudent():
	rmStd = input("Enter Student Roll No. To Remove: ")
	mycursor.execute("(SELECT count(1) FROM students WHERE RollNo = %(rollno)s )",{'rollno':rmStd})
	if mycursor.fetchone()[0]:
		mycursor.execute("DELETE FROM students WHERE RollNo = %(rollno)s",{'rollno':rmStd})
		mydb.commit()
		print("\nStudent {} Successfully Deleted from Database \n".format(rmStd))
	else:
		print("\nNo Record Found of This Student {}".format(rmStd)) #Error Message	

def DelCourse():		
	rmStd = input("Enter Course To Remove: ")
	mycursor.execute("(SELECT count(1) FROM course WHERE CourseName = %(cn)s )",{'cn':rmStd})
	if mycursor.fetchone()[0]:
		mycursor.execute("DELETE FROM course WHERE CourseName = %(cn)s",{'cn':rmStd})
		mydb.commit()
		print("\nCourse {} Successfully Deleted from Database \n".format(rmStd))
	else:
		print("\nNo Record Found of This Course {}".format(rmStd)) #Error Message
		
def DelDept():
	rmStd = input("Enter Department To Remove: ")
	mycursor.execute("(SELECT count(1) FROM department WHERE DeptName = %(dn)s )",{'dn':rmStd})
	if mycursor.fetchone()[0]:
		mycursor.execute("DELETE FROM department WHERE DeptName = %(dn)s",{'dn':rmStd})
		mydb.commit()
		print("\nDepartment {} Successfully Deleted from Database \n".format(rmStd))
	else:
		print("\nNo Record Found of This Department {}".format(rmStd)) #Error Message

def AdminLogIn():
	count=1
	while True:
		au = input('\nENTER ADMIN USER NAME: ')
		au = au.lower()
		ap = str(getpass.getpass('ENTER ADMIN Password: '))
		ap = ap.lower()
		mycursor.execute("(SELECT count(1) FROM admin WHERE AU = %(name)s  AND AP = %(psd)s)",{'name':au,'psd':ap})
		#mycursor2.execute("(SELECT count(1) FROM users WHERE password = %(pwd)s )",{'pwd':pwd})
		if mycursor.fetchone()[0]:
			return True
		elif count < 3:
			count=count+1
			print('----------------')
			print('****************')
			print('INVALID ADMIN USERNAME OR PASSWORD')
			print('****************')
			print('----------------')
			
		else:
			print('-----------------------------------')
			print('***********************************')
			print('3 UNSUCCESFUL ATTEMPTS, EXITING')
			print('!!!!!YOU HAS BEEN LOCKED!!!!!')
			print('***********************************')
			print('-----------------------------------')
			print('')
			fp = input('Forgot Admin password? (Y/N) : ')
			fp = fp.lower()
			if fp == "y":
				user = input('\nENTER ADMIN USER NAME: ')
				user = user.lower()
				mycursor.execute("(SELECT count(1) FROM admin WHERE AU = %(name)s )",{'name':user})
				if mycursor.fetchone()[0]:
					npwd = input('\nENTER Password: ')
					npwd = npwd.lower()
					mycursor.execute("UPDATE admin SET AP = %(up)s WHERE AU = %(un)s",{'up':npwd, 'un':user})
					mydb.commit()
					print("ADMIN Password has been changed successfully!")
					LogIn()
				else:
					print('ADMIN Username not in database.')
					return False
					
			else:
				print(os.system('cls'))
				LogIn()
	
	
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
	Enter 7 : To Log Out
		
		""")

	try: #Using Exceptions For Validation
		userInput = int(input("Please Select An Above Option: ")) #Will Take Input From User
	except ValueError:
		exit("\nHy! That's Not A Number") #Error Message
	else:
		print("\n") #Print New Line

	#Checking Using Option	
	if(userInput == 1): #This Option Will Print List Of Students
		mycursor.execute("(SELECT count(1) FROM students)")
		if mycursor.fetchone()[0]:
			print("List Students\n") 
			
			mycursor.execute("SELECT s.RollNo, s.FirstName, s.LastName, s.Phone, s.Gmail, d.DeptName,d.DeptHOD, c.CourseName, c.CourseId  FROM students s, course c, department d where s.CourseName=c.CourseName AND c.CourseDept=d.DeptName")
			vin = mycursor.fetchall()
			i=1
			print("SN\tRoll no.\tName\t\tPhone\t\tGmail\t\tDepartment \tHOD\tCourse\tC_ID \t")				
			for a, b, c, d, e,f,g,h,j in vin:
				print("{}\t{}\t{} {}\t{}\t{}\t{}\t{}\t{}\t{}".format(i, a, b, c, d, e,f,g,h,j))
				i=i+1
		else:
			print("Database is epmty!\n") 

	elif(userInput == 2): #This Option Will Add New Student In The Database
		flag = True
		while flag == True:
		
			print("Enter new student:\n")
			StdRollno = 0
			while len(str(StdRollno)) != 8:
				try:
					StdRollno = int(input("Enter Roll no: "))
				except ValueError:
					print("Enter Valid roll no.")		
			
			#Checking exixtance
			mycursor.execute("(SELECT count(1) FROM students WHERE RollNo = %(rollno)s )",{'rollno':StdRollno})
			
			if mycursor.fetchone()[0]:
				print("\nThis Student {} Already In The Database".format(StdRollno))
			else: 
				StdFName = input("Enter First Name: ")
				StdLName = input("Enter Last Name: ")
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
				
				while True:
					StdCourse = input("Enter Course: ")			
					mycursor.execute("SELECT count(1) FROM course where CourseName = %(DN)s",{'DN':StdCourse})
					if mycursor.fetchone()[0]==False:
						print("Course Doesn't exits!")
						ask=input("Do you want to add? Y/N ")
						if ask.lower() =='y':
							AddCourse()##Function for add new department
							break
						else:
							manageStudent()
					else:
						break
				
				Course_for_student=StdCourse										
				mycursor.execute("INSERT INTO students (RollNo, FirstName, LastName, Gmail, Phone, CourseName) VALUES (%(rollno)s, %(Fname)s, %(Lname)s, %(gmail)s, %(phone)s, %(Cname)s)", {'rollno':StdRollno, 'Fname':StdFName, 'Lname':StdLName, 'gmail':StdGmail, 'phone':StdPhone, 'Cname':Course_for_student})
				mydb.commit() #Save data on databse
				
				print("\n New Student {} Successfully Added \n".format(StdRollno))	
				N=6
				while True:
					res1=''.join(random.choices(string.ascii_uppercase+'', k=N))
					mycursor.execute("SELECT count(1) FROM users WHERE UN = %(un)s",{'un':str(res1)})
					if mycursor.fetchone()[0]:
						pass
					else:
						break
				
				while True:
					res2=''.join(random.choices(string.ascii_uppercase+'', k=N))
					mycursor.execute("SELECT count(1) FROM users WHERE UP = %(up)s",{'up':str(res2)})
					if mycursor.fetchone()[0]:
						pass
					else:
						break	
							
				mycursor.execute("INSERT INTO users VALUES (%(Rollno)s, %(s1)s, %(s2)s)",{'Rollno':StdRollno, 's1':str(res1), 's2':str(res2)})	
				mydb.commit()
				
				ask = input("Do you want to add student more?(y) ")
				if ask.lower()=='y':
					pass
				else:
					flag=False
		manageStudent()
		
	elif(userInput == 3): #This Option Will Search Student From The List
		flag = True
		while flag == True:
			print(""" 
	Search By?
	Enter 1 : Search By Name 
	Enter 2 : Search By Roll No
	Enter 3 : Previous Menu
		
		""")
			ss=input("Your choice? ")
			if str(ss)=='1':
				srcStd = input("Enter Student Name To Search: ")
				mycursor.execute("(SELECT count(1) FROM students WHERE FirstName = %(name)s )",{'name':srcStd})
			
				if mycursor.fetchone()[0]:
					print("\nRecord Found Of Student {}".format(srcStd))
				else:
					print("\nNo Record Found Of Student {}".format(srcStd)) #Error Message
			elif(str(ss)=='2'):
				srcRoll = input("Enter Student Roll no To Search: ")
				mycursor.execute("(SELECT count(1) FROM students WHERE RollNo = %(rollno)s )",{'rollno':srcRoll})
			
				if mycursor.fetchone()[0]:
					print("\nRecord Found Of Student {}".format(srcRoll))
				else:
					print("\nNo Record Found Of Student {}".format(srcRoll)) #Error Message
			elif(str(ss)=='3'):
				print(os.system('cls'))
				manageStudent()			
			#else:
				#print(os.system('cls'))
				#LogIn()
			ask = input("Do you want to search records more?(y) ")
			if ask.lower()=='y':
				pass
			else:
				flag=False
		manageStudent()		

	elif(userInput == 4): #This Option Will Remove Student From The List
		f=True
		while f==True:
			print("What do yo want to delete recods! ")
			print("1. Department")
			print("2. Course")
			print("3. Student")
			print("3<. exits")
			ask=int(input("Your choice? "))
			if ask==1:
				DelDept()##Function
			elif ask==2:
				DelCourse()#Function
			elif ask==3:
				DelStudent()#Function
			else:
				print("Invalid Choice!  ")
				f=False
		manageStudent()
		
	elif(userInput == 5):
		flag=True
		while flag == True:			
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
			
			mycursor.execute("(SELECT count(1) FROM students)")
			if mycursor.fetchone()[0]:
				print("List Students\n") 
				
				mycursor.execute("SELECT s.RollNo, s.FirstName, s.LastName, s.Phone, s.Gmail, d.DeptName,d.DeptHOD, c.CourseName, c.CourseId  FROM students s, course c, department d where s.CourseName=c.CourseName AND c.CourseDept=d.DeptName ORDER BY s.RollNo %s, s.FirstName %s" %(para1, para2))
				vin = mycursor.fetchall()
				i=1
				print("SN\tRoll no.\tName\t\tPhone\t\tGmail\t\tDepartment \tHOD\tCourse\tC_ID \t")				
				for a, b, c, d, e,f,g,h,j in vin:
					print("{}\t{}\t{} {}\t{}\t{}\t{}\t{}\t{}\t{}".format(i, a, b, c, d, e,f,g,h,j))
					i=i+1
			else:
				print("Database is epmty!\n") 

			ask = input("Do you want to sort again?(y) ")
			if ask.lower()=='y':
				pass
			else:
				flag=False
		manageStudent()
			
	elif(userInput == 6):	
		flag=True
		while flag == True:	
			print("What do yo want to Update! ")
			print("1. Student")
			print("2. Course")
			print("3. Department")
			print("3<. exits")
			ask2=int(input("Your choice? "))
			if ask2 == 1:
				#mycursor.execute("(SELECT count(1) FROM students)")
				UpStdRollno = 0
				while len(str(UpStdRollno)) != 8:
					try:
						UpStdRollno = int(input("Enter Roll no: "))
					except ValueError:
						print("Enter Valid roll no.")		
				
				#Checking exixtance
				mycursor.execute("(SELECT count(1) FROM students WHERE RollNo = %(rollno)s )",{'rollno':UpStdRollno})
				
				if mycursor.fetchone()[0]:
					#print("\nThis Student {} Already In The Database".format(UpStdRollno))
				#else: 
					UpStdFName = input("Enter First Name: ")
					UpStdLName = input("Enter Last Name: ")
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
					c=0
					UpStdCourse=None
					while True :
						UpStdCourse = input("Enter Course: ")			
						mycursor.execute("SELECT count(1) FROM course where CourseName = %(DN)s",{'DN':UpStdCourse})
						if c > 3 :
							print("Update Unsuccessfull !")
							manageStudent()
						elif mycursor.fetchone()[0]==False:
							print("Enter Valid course Name! ")
							c=c+1
						else:
							break		
													
					mycursor.execute("UPDATE students SET FirstName = %(Fname)s, LastName=%(Lname)s, Gmail=%(gmail)s, Phone=%(phone)s, CourseName=%(Cname)s WHERE students.RollNo=%(roll)s", { 'Fname':UpStdFName, 'Lname':UpStdLName, 'gmail':UpStdGmail, 'phone':UpStdPhone, 'Cname':UpStdCourse, 'roll':UpStdRollno})
					mydb.commit() #Save data on databse
					print("Roll no. {} Updated successfully!".format(UpStdRollno))
				else:
					print("Roll no {} doesn't exists!".format(UpStdRollno))
					
			elif ask2 == 2:
				UpCourse = None
				while UpCourse == None:
					try:
						UpCourse = input("Enter Course: ")
					except ValueError:
						print("Enter Valid Course")		
				
				#Checking exixtance
				mycursor.execute("(SELECT count(1) FROM course WHERE CourseName = %(cn)s )",{'cn':UpCourse})
				
				if mycursor.fetchone()[0]:
					#print("\nThis Student {} Already In The Database".format(UpStdRollno))
				#else: 
					UpCourseId = input("Enter Course Id: ")
					UpCourseFee = input("Enter Course fee: ")
					UpCourseDuration = input("Enter Course Duration: ")
					c=0
					UpCourseDept=None
					while True :
						UpCourseDept = input("Enter Department: ")			
						mycursor.execute("SELECT count(1) FROM department where DeptName = %(DN)s",{'DN':UpCourseDept})
						if c > 3 :
							print("Update Unsuccessfull !")
							manageStudent()
						elif mycursor.fetchone()[0]==False:
							print("Enter Valid Department Name! ")
							c=c+1
						else:
							break		
													
					mycursor.execute("UPDATE course SET CourseId = %(ci)s, CourseFee =%(cf)s, CourseDuration=%(cd)s, CourseDept=%(cd2)s WHERE course.CourseName=%(cn)s", { 'ci':UpCourseId, 'cf':UpCourseFee, 'cd':UpCourseDuration, 'cd2':UpCourseDept, 'cn':UpCourse})
					mydb.commit() #Save data on databse
					print("Course {} Updated successfully!".format(UpCourse))
				else:
					print("Course {} doesn't exists!".format(UpCourse))
			elif ask2 == 3:
				UpDept = None
				while UpDept == None:
					try:
						UpDept = input("Enter Department: ")
					except ValueError:
						print("Enter Valid Department")		
				
				#Checking exixtance
				mycursor.execute("(SELECT count(1) FROM department WHERE DeptName = %(dn)s )",{'dn':UpDept})
				
				if mycursor.fetchone()[0]:
					UpDeptCode = input("Enter department Code: ")
					UpDeptHod = input("Enter Department HOD: ")
					UpDeptEmp = input("Enter no of employees: ")
					c=0
					
					mycursor.execute("UPDATE department SET DeptCode = %(dc)s, DeptHOD =%(dh)s, DeptEmp=%(de)s WHERE department.DeptName=%(dn)s", { 'dc':UpDeptCode, 'dh':UpDeptHod, 'de':UpDeptEmp, 'dn':UpDept})
					mydb.commit() #Save data on databse
					print("Department {} Updated successfully!".format(UpDept))
				else:
					print("Department {} doesn't exists!".format(UpDept))
			
			else:
				manageStudent()
				
			ask = input("Do you want to sort again?(y) ")
			if ask.lower()=='y':
				pass
			else:
				flag=False
		manageStudent()	
		
	elif(userInput == 7):
		print("LogOut Successfully! ")
		LogIn()
	
	elif(userInput < 1 or userInput > 7): #Validating User Option
		print("Please Enter Valid Option")	#Error Message
	
	
	
	#manageStudent()
					
def UserInfo(info):
		a,b,c,d,e,f,g,h = info
		print("""
				 #####################################################################
				######################## Welcome {} ###################################
		
			   ####        	Name:{} {} 					Roll No.: {}        	#########
			   ####			Gmail: {}											#########
			   ####			Course: {}	            	Phone: {}			    #########
			   ####			Department: {}				HOD: {}   				#########
			   **************************************************************************
			   """.format(b,b,c,a,d,f,e,g,h))
		
		
		while True:
			ch = input("Enter 'y' to LogOut: ")
			if ch == 'y':
				print(os.system('cls'))
				LogIn()
			else:
				print("Invalid Choice")
		#else:
		print("Sorry You are deleted!")
		LogIn()
					
def LogIn():
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

	Enter 1 : User Login 
	Enter 2 : Admin Login
	Enter 3 or  : Exit 
		
		""")
	try: #Using Exceptions For Validation
		userInput = int(input("Please Select An Above Option: ")) #Will Take Input From User
	except ValueError:
		exit("\nHy! That's Not A Number") #Error Message
	else:
		print("\n") #Print New Line

	#Checking Using Option	
	count=1
	if(userInput == 1):
		while True:
			user = input('\nENTER USER NAME: ')
			user = user.lower()
			pwd = str(getpass.getpass('ENTER Password: '))
			pwd = pwd.lower()
			mycursor.execute("(SELECT count(1) FROM users WHERE UN = %(name)s  AND UP = %(psd)s)",{'name':user,'psd':pwd})
			#mycursor2.execute("(SELECT count(1) FROM users WHERE password = %(pwd)s )",{'pwd':pwd})
			if mycursor.fetchone()[0]:
				mycursor.execute("(SELECT RollNo FROM users WHERE UN = %(name)s  AND UP = %(psd)s)",{'name':user,'psd':pwd})
				roll=mycursor.fetchone()
				mycursor.execute("(SELECT u.RollNo, s.FirstName, s.LastName, s.Gmail, s.Phone,c.CourseName, d.DeptName, d.DeptHOD FROM users u, students s, department d, course c WHERE s.RollNo = %s AND s.RollNo=u.RollNo AND c.CourseDept=d.DeptName AND s.CourseName=c.CourseName)",(roll))
				info=mycursor.fetchone()
				UserInfo(info)
				break
			elif count < 3:
				count=count+1
				print('----------------')
				print('****************')
				print('INVALID USERNAME OR PASSWORD')
				print('****************')
				print('----------------')
				
			else:
				print('-----------------------------------')
				print('***********************************')
				print('3 UNSUCCESFUL ATTEMPTS, EXITING')
				print('!!!!!YOU HAS BEEN LOCKED!!!!!')
				print('***********************************')
				print('-----------------------------------')
				print('')
				fp = input('Forgot password? (Y/N) : ')
				fp = fp.lower()
				if fp == "y":
					user = input('\nENTER USER NAME: ')
					user = user.lower()
					mycursor.execute("(SELECT count(1) FROM users WHERE UN = %(name)s )",{'name':user})
					if mycursor.fetchone()[0]:
						npwd = input('\nENTER Password: ')
						npwd = npwd.lower()
						mycursor.execute("UPDATE users SET UP = %(up)s WHERE UN = %(un)s",{'up':npwd, 'un':user})
						mydb.commit()
						print("Password has been changed successfully!")
						LogIn()
					else:
						print('Username not in database.')
						break
						
				else:
					print(os.system('cls'))
					LogIn()
					
	if(userInput == 2):
		if AdminLogIn()==True:
			manageStudent()
		else:
			print("Invalid access")
			LogIn()
	else:
		quit("Bye Bye")


def runAgain(): #Making Runable Problem1353
	runAgn = input("\nWant To Run Again Y/N: ")
	if(runAgn.lower() == 'y'):
		if(platform.system() == "Windows"): #Checking User OS For Clearing The Screen
			print(os.system('cls'))
		else:
			print(os.system('clear'))
		manageStudent()
		runAgain()
	else:
		quit(bye) #Print GoodBye Message And Exit The Program
LogIn()
runAgain()		
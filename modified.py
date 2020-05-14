# ################### Module imports ######################### #
from tkinter import *
from tkinter import messagebox
from datetime import date
from datetime import datetime
from PIL import Image , ImageTk
''' for Opening web browser '''
import webbrowser 
import time
''' Importing data base module  ''' 
import sqlite3 

# ############################## INITIALIZING DATA BASE ######################### #
conn = sqlite3.connect('my_db.db')
''' cursor to search and add items in data base '''
c = conn.cursor()

''' Making table in data base '''
try: 
  c.execute("""CREATE TABLE person (
            name text,
            title text,
            Time_ text, 
            dat_ text,
            url_ text
            )""")
except:
  pass 
def insert_schedule(obj): ######## inserting items ##############
    with conn:
        c.execute("INSERT INTO person VALUES (:name, :title, :Time_, :dat_ ,:url )", {'name':obj.name, 'title':obj.title, 'Time_':obj._time_, 'dat_':obj.d , 'url':obj.url })   
def get_schedule_by_name(): ########## #QUERYING DATA BASE TO FIND ITEMS ##################### 
	c.execute("SELECT * FROM person ")
	return c.fetchall()
# ###################################### Classes and funtions ###################################### #

class Data: # ############## Data class an object will be made and that object will be stored in data base ################ #
	def __init__(self , name , title , _time_ , url_ , d):
		self.name , self.title , self._time_ , self.url = name , title , _time_ , url_
		self.d = d
	def info(self): # ############# Returns objects properties to be stored in respective columns ################ #
		self.tup = (self.name , self.title , self._time_ , self.url, self.d)
		return 	self.tup

class Buttons:
	itr ,  data = [] , []  
	rec  , rec_1 , counter , counter_2 = [ (10,350) ] , [ (10,400) ] , 0 , 0
	def __init__(self, root , row , col , txt , bg , obj , obj2, url_ , fg = 'Black'  , size = 10):
		self.root , self.row , self.col = root , row , col
		self.txt = txt
		self.bg  , self.fg = bg , fg
		self.obj , self.obj2 = obj , obj2
		self.url_ , self.size = url_ , size
		if self.txt.split(' ')[0] == '0':  
			self.txt = '12'+' '+self.txt.split(' ')[-1]
		else:
			self.txt = txt	
		self.bt = Button(self.root , text = self.txt , bg = self.bg , fg = self.fg , height=  2 , width = 10,  font = ('verdana' , self.size) , command = self.go)
		self.bt.place(x = self.row , y = self.col)
	def give_info(self):
		if self.bt['text'] not in Buttons.itr:
			Buttons.itr.append(self.bt['text'])
	def change(self): # ############# When a button is clicked it makes a Label of same text in Selected times bar at bottom of main window ############ #
		if Buttons.counter >= 5 and Buttons.counter_2 >= 5:
			return False		
		if self.bt['text'] not in Buttons.data:		
			if Buttons.counter > 4:
				Buttons.data.append(self.bt['text'])
				self.L = Labels(self.root, self.bt['text'] , Buttons.rec_1[ Buttons.counter_2 ][0] , Buttons.rec_1[ Buttons.counter_2 ][1]  , size = 12 )
				Buttons.rec_1.append( (self.L.row+95 , 400)  )
				Buttons.counter_2+=1
			if Buttons.counter <= 4:
				Buttons.data.append(self.bt['text'])
				self.L = Labels(self.root, self.bt['text'] , Buttons.rec[ Buttons.counter ][0] , Buttons.rec[ Buttons.counter ][1]  , size = 12 )
				Buttons.rec.append( (self.L.row+95 , 350) )
			Buttons.counter+=1
			Labels.count = True
	def go(self):
		if self.obj != None :
			Buttons.d , Buttons.d2 = self.obj.get() , self.obj2.get() 	
			if Buttons.d != '' and Buttons.d2 !='':
				self.give_info()
				self.change()
			else:
				messagebox.showinfo('Credential Error ' , 'Please Enter Your name and Title of meeting')	
		else:
			self.open_url()		
	def open_url(self): # ###### Fuction takes URL and open it in google chrome when clicked in new tab #############
		webbrowser.open(self.url_)

class Labels:
	count= False
	def __init__(self , root , txt , row , col, size = 10):
		self.root , self.txt , self.row , self.col = root , txt , row , col
		self.lab = Label(self.root , text = self.txt , height = 2  , width = 5,fg = 'Gold' , bg = 'darkRed' , font = ('verdana' , size))
		self.lab.place(x = self.row , y = self.col)
	
def set_it(nam , txt , time_new , date_url , time_url): # ########## SET URL in required format to use ########## #
	if time_new == 24:
		url = 'https://calendar.google.com/calendar/r/eventedit?text='+txt+'&dates='+'20200520T070000Z/20200520T080000Z'+'&location=https://whereby.com/sam-ie'
		my_obj = Data(nam , txt , time_url , url , date_url)
		insert_schedule(my_obj)
		return url
	else:
		url = 'https://calendar.google.com/calendar/r/eventedit?text='+txt+'&dates='+date_url.strip()+'T'+str(time_new)+'0000'+'/'+date_url.strip()+'T'+str(time_new+1)+'0000'+'&location=https://whereby.com/sam-ie'
		my_obj = Data(nam , txt , time_url , url , date_url)
		insert_schedule(my_obj)	    
		return url



class New:   # ##################################### Second window with links 
	dic  , new_lis  , new_col = {} , [] , 120
	new_col_2 = 120
	my_lis ,  initial =[] ,  0
	my = []
	def __init__(self  , root  ,  text , name , dat):
		self.root = root
		self.text , self.name , self.dat = text , name , dat
		self.root.destroy()
		self.app = Tk()
		self.app.geometry('600x580')
		self.app.resizable(0,0)
		Label(self.app , text = 'Your sessions have been scheduled Succesfully !\n\n Here are the links check them out  ' , fg = 'Gold' , bg = 'Maroon'  , font = ('verdana' , 14)).place(x = 40 , y = 0)
		Button(self.app , text = 'BACK', bg = 'Red',fg = 'Gold' , font = ('Italian' , 12) , command = lambda : create_new_wind(self.app)).place(x = 20 , y = 530)
		Button(self.app , text = 'EXIT', bg = 'Red',fg = 'Gold' , font = ('Italian' , 12) , command = lambda : exit()).place(x = 540 , y = 530)
		Label(self.app , text = 'Links for Your Selected Schedules are : ',bg = 'DarkBlue' , fg = 'Gold' , font = ('Italian' , 12)).place(x = 0 , y = 80)
		for i in range(len(self.dat)): # ######## Creatting labels and buttons for links ############# #
			if i <= 4 :
				self.url = gen_link(self.name , self.text , self.dat[i] )
				if type(self.url) == type(tuple()):
					Label(self.app , text = self.dat[i]+' :' ,bg = 'Black' , fg = 'white' ,font = ('verdana' , 8) ).place(x = New.initial , y = New.new_col)
					New.my_lis.append(Buttons(self.app , New.initial+80 , New.new_col , 'OPEN LINK ! ' , 'Red' , None , None ,self.url[0] , size = 6 ))
					Label(self.app , text = self.url[-1] , fg = 'white' , bg = 'Black' , font =('verdana' , 7)).place(x =New.initial , y = New.new_col+35)
					New.new_col+=80
				else:
					Label(self.app , text = self.dat[i]+' :' ,bg = 'Black' , fg = 'white' ,font = ('verdana' , 8) ).place(x = New.initial , y = New.new_col)
					New.my_lis.append(Buttons(self.app , New.initial+80 , New.new_col , 'OPEN LINK ! ' , 'Red' , None , None ,self.url , size = 6 ))
					New.new_col+=80
			if i > 4:
				self.url = gen_link(self.name , self.text , self.dat[i] )
				if type(self.url) == type(tuple()):
					Label(self.app , text = self.dat[i]+' :' ,bg = 'Black' , fg = 'white' ,font = ('verdana' , 8) ).place(x = New.initial+250 , y = New.new_col_2)
					New.my_lis.append(Buttons(self.app , New.initial+330 , New.new_col_2 , 'OPEN LINK ! ' , 'Red' , None , None ,self.url[0] , size = 6 ))
					Label(self.app , text = self.url[-1] , fg = 'white' , bg = 'Black' , font =('verdana' , 7)).place(x =New.initial+250 , y = New.new_col_2+35)
					New.new_col_2+=80
				else:	
					Label(self.app , text = self.dat[i]+' :' ,bg = 'Black' , fg = 'white' ,font = ('verdana' , 8) ).place(x = New.initial+250 , y = New.new_col_2)
					New.my_lis.append(Buttons(self.app , New.initial+330 , New.new_col_2 , 'OPEN LINK ! ' , 'Red' , None , None ,self.url , size = 6 ))	
					New.new_col_2+=80
		self.app.mainloop()

def create_new_wind(app):  # ############ Attached to BACK button it destrys recent window and goes back to main window
	app.destroy()
	reset() ####### #Initializing every thing
	my_wind  = Main()	 ##### Object of main window

def gen_link(nam , txt, time_url ): # ########## Generating URL for LINKS it is atached to buttons with links of meeting in New window class ############# # 
# ###### Getting DATE in required format # #################
  now = datetime.now() 
  dt_string = now.strftime("%Y:%m:%d : %H:%M:%S")
  z = dt_string.split(':')
  date_url = z[0]+z[1]+z[2]
  time_new = int(time_url.split(' ')[0]) + 12

##############  Checking DATA BASE IF THERE IS ALEADY ANOTHER ENTRY WITH SAME TITLE OR NOT  ##############

  emp =  get_schedule_by_name()
  if emp == None:  
	  set_it(nam , txt , time_new , date_url , time_url)
  else:
  	z = []
  	z = get_schedule_by_name()
  	for k in z:
  		if k[1]== txt and k[2]== time_url and k[3] == date_url:
  			msg = 'YOUR SESSION IS SCHEDULED WITH '+k[0]+'\n'+' at '+k[2]+' on same topic of '+k[1]
  			url = k[-1]
  			g = (url , msg )
  			return g
  	my_url = set_it(nam , txt , time_new , date_url , time_url)
  	return my_url		  	

def sch(e , e2 , root): # ########################### Generates NEW window this function is attached to Schedule button on main window
	if e.get() != '' and e2.get() != ' ' and Labels.count==True:
		# print(Buttons.data)
		n = New(root , e2.get() , e.get() , Buttons.data) # ####### making an object of new window
	else:	
		messagebox.showinfo('Credential Error' , 'Please select Time frame ! ')

# ############################ DYNAMIC LINKS ############################## #

format = '%H:%M %p'
time_ = time.strftime('%H:%M')
# print(time_) # ############################# 24 HOUR TIME ############################### #
m = '12:00'  
my_date = datetime.strptime(time_+' '+'pm', format)
tim = my_date.strftime(format)
# print(tim)
tim_2 = tim.split(' ') # ############# String manipulation  to get time and date in required fomat ############ #
tim_3 = tim_2[0].split(':')

''' Checking if the time is before 12 PM or exactly 12 PM or wether it is after 9PM after which day ends '''
if ( (tim_2[-1] == 'PM') and (tim_3[0] == '12' and tim_3[1] == '00') ) or (tim_2[-1] == 'AM') or ((tim_2[-1] == 'PM') and (tim_3[0] == '21' or tim_3[0] == '22' or tim_3[0] == '23' )):
	mark = True
	deli = 10

else: # ############ If It is in  middle of day so it will show remaining times available ###############	
	y = int(tim_3[0]) - 12 
	print(y)
	deli = 9-y
	mark = False
	print(deli)

# print(tim_2)
# print(tim_3)

def create_bt(root , obj , obj2 , x , mr):  #  Creating objects from Buttons class according to the time left
	global lis , lis_2
	lis , lis_2 , c  = [] ,[], 200  
	if x > 5 :
		if mr == True:
			num = 0
		else:	
			num = (int(tim_3[0]) - 12)+1
		ran = 2
		for i in range(ran):
			k = 10  
			for j in range(5):	
				lis.append(Buttons(root ,  k , c , str(num)+' PM' , 'Purple' ,  obj , obj2, None ,'Gold' ))
				if num == 9 :
					break
				k+=95
				num+=1
			c += 50
	elif y<=5:
		ran = 1
		num = 5
		for i in range(ran):
			k = 10  
			for j in range(5):	
				lis.append(Buttons(root ,  k , c , str(num)+' PM' , 'Purple' ,  obj , obj2, 'Gold' ))
				k+=95
				num+=1
			c += 50


# ############################ DYNAMIC LINKS ############################## #

today = date.today()  # ######## Getting system time
date_ = today.strftime("%B %d, %Y")

def reset(): # ################### INITIALIZING EVERY THING TO START after pressing the back button ########################### #
	lis , lis_2 , Buttons.data =  [] , [] , []
	Buttons.rec  , Buttons.rec_1 , Buttons.counter , Buttons.counter_2 = [ (10,350) ] , [ (10,400) ] , 0 , 0
	Buttons.itr ,  Buttons.data = [] , []  
	New.dic  , New.new_lis , New.new_col , New.new_col_2= {} , [] , 120 , 120
	New.my_lis = []
	Labels.lis_3 = []

class Main:    # ################## Main window to select time and topic
	def __init__(self):
		self.wind = Tk()

		self.wind.geometry('500x500')
		self.img = Image.open('bg.png')
		self.img = self.img.resize((500,500), Image.ANTIALIAS) 
		self.photo_1 = ImageTk.PhotoImage(self.img)
		self.label_1 = Label(self.wind , image = self.photo_1)
		self.label_1.pack()
		Label(self.wind , text = 'ATTENTIONHub' , bg = 'Red' ,font = ('verdana' , 15) ).place(x = 175,y = 0)
		Label(self.wind , text = 'Name ' , font = ('verdana' , 11) ,fg = 'Gold', bg = 'DarkBlue').place(x = 0 , y = 90)
		self.e = Entry(self.wind,  font = ('verdana' , 11))
		self.e.place(x = 65 , y = 90)
		Label(self.wind , text = 'Title    ' , font = ('verdana' , 11),fg = 'Gold' , bg = 'DarkBlue').place(x = 0 , y = 120)
		self.e2 = Entry(self.wind , font = ('verdana' , 11))
		self.e2.place(x = 65 , y = 120)
		Label(self.wind , text = 'Today : '+date_ , fg = 'Gold' , bg = '#0095B6' , font = ('verdana' , 13)).place(x = 0 , y = 50)
		Label(self.wind , text = 'Available Schedules : ' , fg = 'Gold' , bg = '#0095B6' , font = ('verdana' , 13)).place(x = 0 , y = 160)
		Label(self.wind , text = 'Meeting Times :' , fg = 'Gold' , bg = '#0095B6' , font = ('verdana' , 13)).place(x = 0 , y = 310)
		self.click_me = Button(self.wind , text = 'Schedule Me'  , bg = 'pink' , fg = 'DarkBlue',height = 2 , width = 10 , font=('verdana' , 12) , command = lambda : sch(self.e , self.e2 , self.wind))
		self.click_me.place(x = 200 , y = 450 )
		create_bt(self.wind , self.e,  self.e2 ,  deli  , mark)

		self.wind.mainloop()

# ########### MAIN ############ #

prog = Main()

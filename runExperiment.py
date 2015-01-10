#!/usr/bin/env python
import numpy as np
import os
import cv
import cv2
import csv
import time
import sys
from subprocess import call
from Tkinter import *
import Image
import ImageTk
import transformations
import threading
#import abbSim

# Writen by Trevor Decker 

#TODO add prompt for change of station location 
#TODO have buttons actually change values 
#TODO add simulated robot whith the same interface as the real one 
#TODO add new log folder button 
#TODO add position as a part of the text file 
#TODO mutex shit should get ride of color change in image stream 

sys.path.insert(0, 'abb/open-abb-driver/abb_node/packages/abb_communications')
import abb

def getImage(cap):
    ret, frame = cap.read();
    filePATH = "tempTestFile_IDoNotNeed.jpg"
    cv2.imwrite(filePATH,frame)
    return Image.open(filePATH)

def updateGUI(gui,cap):
    global imLabel
    newImage = getImage(cap)
    photo = ImageTk.PhotoImage(newImage)
    imLabel.image = photo
    imLabel.configure(image=photo)

def updateIMG():
    global mutex
    while True:
#        mutex.acquire()
        img = ImageTk.PhotoImage(getImage(cap))
        imLabel.configure(image = img)
        imLabel.image = img
 #       mutex.release()
        time.sleep(.05)

def moveTo(R,x,y,z,x_rot,y_rot,z_rot):
    q = transformations.quaternion_from_euler(x_rot, y_rot, z_rot, axes='sxyz')
    A = R.get_cartesian()
    q = A[1]
    p = [x,y,z]
    pose_to_send = [p,q]
    print "moveTo \n"
    print (transformations.euler_from_quaternion(pose_to_send[1],'sxyz'))
    print pose_to_send
    R.set_cartesian(pose_to_send)
    time.sleep(1)
       
def processImage(R,station,i,cap,directory):
    global ImageId
    global ImageId_lock
 #   ImageId_lock.acquire()
    ImageId = ImageId + 1
  #  ImageId_lock.release()
    ret, frame = cap.read();
    cartesian =  R.get_cartesian()
    position = cartesian[0]
    quad = cartesian[1]
    x = position[0]
    y = position[1]
    z = position[2]
    q_0 = quad[0]
    q_1 = quad[1]
    q_2 = quad[2]
    q_3 = quad[3]
    
    print "cap.read state " + str(ret)
    #station = str(station)
   # i = str(i)
    imgFile = directory+'/'+str(ImageId)+'.jpg'
    txtFile = directory+'/'+str(ImageId)+'armState.txt'
    text_file = open(txtFile,"w")
    text_file.write("x,"+str(x) + "\n")
    text_file.write("y,"+str(y) + "\n")
    text_file.write("z,"+str(z) + "\n")
    text_file.write("q_0,"+str(q_0) + "\n")
    text_file.write("q_1,"+str(q_1) + "\n")
    text_file.write("q_2,"+str(q_2) + "\n")
    text_file.write("q_3,"+str(q_3) + "\n")
    text_file.close()
    cv2.imwrite(imgFile,frame)
    call(["./apriltags_demo",imgFile])
 
#returns the new directory's relative path 
def newLogFolder():
    #creates a folder to store all of the images 
    directory = 'log_files/'+str(time.time())
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def logCurrentState(R,directory):
      station = -1
      i = -1
      processImage(R,station,i,cap,directory)
  

def collectData(R,directory):
    global useRealRobot
    global num_pictures_per_location
    global cap;

    directory = newLogFolder()
    #TODO set capture resolution 
    with open('points.csv', 'rb') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        count = 0
        for row in rowreader:
            count=count+1
        total = count

    with open('points.csv','rb') as csvfile:
        rowreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        count = 0
        for row in rowreader:
            count=count+1
            print count/total 
            thisRow = row[0].split(',')
            x = float(thisRow[0])
            y = float(thisRow[1])
            z = float(thisRow[2])
            x_rot = float(thisRow[3])
            y_rot = float(thisRow[4])
            z_rot = float(thisRow[5])
            station = int(thisRow[6])
            if(useRealRobot):
                moveTo(R,x,y,z,x_rot,y_rot,z_rot);
            for i in xrange(0, num_pictures_per_location):
                processImage(R,station,i,cap,directory)
                
            print('DONE at position x %f y %f z %f x_rot %f y_rot %f z_rot %f station %d\n'% (x,y,z,x_rot,y_rot,z_rot,station))
                   
def movePosition(R,position_curr,changed_index,delta):
        global gui
        global cap
        position_curr[changed_index] += delta

        #if changed value was a euler angle we need to convert back to the quadtrnion 
        if changed_index > 6:
            x_rot = position_curr[7]
            y_rot = position_curr[8]
            z_rot = position_curr[9]
            quad = transformations.quaternion_from_euler(x_rot, y_rot, z_rot, axes='sxyz')
            position_curr[4] = quad[0]
            position_curr[5] = quad[1]
            position_curr[6] = quad[2]
            position_curr[7] = quad[3]

        #change format of position_curr to what abb needs
        point = position_curr[0:3]
        A = R.get_cartesian()
        quad =  A[1]#position_curr[3:7]
        print "quad \n"
        print quad
        print transformations.euler_from_quaternion(quad,axes='sxyz')
        pose_to_send = [point,quad]
        print R.get_cartesian()
        print pose_to_send
        global mutex
 #       mutex.acquire()
        R.set_cartesian(pose_to_send)
 #       mutex.release()
        updateGUI(gui,cap)

def moveJoint(R,axis_curr,changed_index,delta):
        global gui
        global cap
	axis_curr[changed_index] += delta
        print "sending "+str(axis_curr)
        global mutex
#        mutex.acquire()
        R.set_joints(axis_curr)
#        mutex.release()        
        updateGUI(gui,cap)

def addJointControl(R,buttons,axis_curr,jNum):
	axis_1_label = Label(buttons,text="JOINT "+str(jNum))
	axis_1_up_btn = Button(buttons,text="<",command=lambda:moveJoint(R,axis_curr,jNum-1,-1.0))
	axis_1_curr_value  = Label(buttons,text=str(axis_curr[jNum-1])) 
        axis_1_down_btn = Button(buttons,text=">",command=lambda:moveJoint(R,axis_curr,jNum-1,1.0))
	

	axis_1_label.grid(row=1,column=4*(jNum-1)+1)
	axis_1_up_btn.grid(row=2,column=4*(jNum-1)+0)
	axis_1_curr_value.grid(row=2,column=4*(jNum-1)+1)
	axis_1_down_btn.grid(row=2,column=4*(jNum-1)+2)

def addPositionControl(R,buttons,position_curr,name,row,col,i):
	axis_1_label = Label(buttons,text=name)
	axis_1_up_btn = Button(buttons,text="<",command=lambda:movePosition(R,position_curr,i-1,-.1))
	axis_1_curr_value  = Label(buttons,text=str(position_curr[i-1])) 
	axis_1_down_btn = Button(buttons,text=">",command=lambda:movePosition(R,position_curr,i-1,.1))
	axis_1_label.grid(row=row,column=4*(col-1)+1)
        axis_1_up_btn.grid(row=row+1,column=4*(col-1)+0)
        axis_1_curr_value.grid(row=row+1,column=4*(col-1)+1)
        axis_1_down_btn.grid(row=row+1,column=4*(col-1)+2)



def drawGUI(gui,R,cap,axis_curr,position_curr,directory):
        global imLabel 
        image = getImage(cap)
        photo = ImageTk.PhotoImage(image)
        imLabel = Label(image=photo)
        imLabel.image=photo
        imLabel.grid()
        t = threading.Thread(target=updateIMG)
        t.daemon = True
        t.start()
       # photo = ImageTk.PhotoImage(image)
       # label=Label(image=photo)
       # label.image = photo
       # label.
       # cv2.imshow("cam n",frame)
	
        buttons = Frame(gui)
	for jointNum in xrange(1,7):
		addJointControl(R,buttons,axis_curr,jointNum)


	addPositionControl(R,buttons,position_curr,"X",3,1,1)
	addPositionControl(R,buttons,position_curr,"Y",3,2,2)
	addPositionControl(R,buttons,position_curr,"Z",3,3,3)
	addPositionControl(R,buttons,position_curr,"q0",3,4,4)
	addPositionControl(R,buttons,position_curr,"q1",3,5,5)
	addPositionControl(R,buttons,position_curr,"q2",3,6,6)
	addPositionControl(R,buttons,position_curr,"q3",3,7,7)
	addPositionControl(R,buttons,position_curr,"roll",5,1,8)
	addPositionControl(R,buttons,position_curr,"pitch",5,2,9)
	addPositionControl(R,buttons,position_curr,"yaw	",5,3,10)
        buttons.grid()
	b = Button(buttons,text="Collect Data",command=lambda:collectData(R,directory))
	b.grid(row=7,column=0)

#        TODO does not work without global 
#        b1 = Button(buttons,text="new Log Folder",command=lambda:newLogFolder())
#	b1.grid(row=5,column=1)
        
        b2 = Button(buttons,text="log Current State",command=lambda:logCurrentState(R,directory))

	b2.grid(row=7,column=2)


def main():
        global mutex
        global ImageId_lock
        global ImageId
#        mutex = threading.Lock()
 #       ImageId_lock = threading.Lock()
        ImageId = 0;

	global useRealRobot
	global num_pictures_per_location
	global cap;
        global gui
#        global axis_curr
#        global position_curr
        camId = 1;

	axis_curr = [-1,-1,-1,-1,-1,-1]
        position_curr = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
	cap = cv2.VideoCapture(camId)

        directory = newLogFolder();

	# should we test the system or use the real robot?
	# if false then do not try to connect to the real robot
	# if true then do try to connect to  to the real robot
	useRealRobot = True;  

	#number of pictures to take at each location
	num_pictures_per_location = 1;
 


	#connect to the robot 
	print "attempting to connect to the robot arm\n"
	if(useRealRobot):
	        R = abb.Robot(ip='192.168.125.1')
        else:
            pass
#            R = abbSim.Robot()
	print "sucssfully connected to robot the robot arm\n"
	if(useRealRobot):
            cartesian = R.get_cartesian()
            joints = R.get_joints()
            axis_curr = joints
            position = cartesian[0]
            quaternion = cartesian[1]
            position_curr[0] = position[0];
            position_curr[1] = position[1];
            position_curr[2] = position[2];
            position_curr[3] = quaternion[0];
            position_curr[4] = quaternion[1];
            position_curr[5] = quaternion[2];
            position_curr[6] = quaternion[3];
            euler = transformations.euler_from_quaternion(quaternion, axes='sxyz')
            position_curr[7] = euler[0];
            position_curr[8] = euler[1];
            position_curr[9] = euler[2];
            print "start State \n"
            print joints
            print position_curr
		#R.set_tool(self, tool=[[0,0,0], [1,0,0,0]])
                

	gui = Tk()
        drawGUI(gui,R,cap,axis_curr,position_curr,directory)
#	otherButtons.grid(row=2,column=0) #side=TOP)
	mainloop()
        cap.release()
        cv2.destroyAllWindows()

main();

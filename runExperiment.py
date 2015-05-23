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
import abbSim


# Writen by Trevor Decker 

#TODO add prompt for change of station location 
#TODO update joints 
#TODO finish simulated robot whith the same interface as the real one 
#TODO add new log folder button 
#TODO mutex shit should get ride of color change in image stream 
#TODO verify timing of arm stuff 
#TODO handle camera not being avilable 


sys.path.insert(0, 'abb/open-abb-driver/abb_node/packages/abb_communications')
import abb

######################################################
# TODO Description of function
# 
# TODO REQUIRES
#
# TODO ENSURES
######################################################
def get_position_curr(R):
    position_curr = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
    cartesian = R.get_cartesian()
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
    return position_curr

############################################################
# Description: ucaptures an image from camrea cap was inilized with,
#              returns the iamge as python Image 
# 
# TODO REQUIERS
# 
# TODO ENSURES 
########################################################### 

def getImage(cap):
    ret, frame = cap.read();
    filePATH = "tempTestFile_IDoNotNeed.jpg"
    cv2.imwrite(filePATH,frame)
    return Image.open(filePATH)

#############################################################
# Description: updates the values in the gui
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################
def updateGUI(R,gui,cap,joint_labels,position_labels):
    global imLabel
    joint_values = R.get_joints()
    position_values = R.get_cartesian()
    position = position_values[0]
    quaternion = position_values[1]
    position_labels[0].config(text = str(position[0]))
    position_labels[1].config(text = str(position[1]));
    position_labels[2].config(text = str(position[2]));
    position_labels[3].config(text = str(quaternion[0]));
    position_labels[4].config(text = str(quaternion[1]));
    position_labels[5].config(text = str(quaternion[2]));
    position_labels[6].config(text = str(quaternion[3]));
    euler = transformations.euler_from_quaternion(quaternion, axes='sxyz')
    position_labels[7].config(text = str(euler[0]));
    position_labels[8].config(text = str(euler[1]));
    position_labels[9].config(text = str(euler[2]));


    for jointNum in xrange(0,6):
        joint_labels[jointNum].config(text = str(joint_values[jointNum]))
        


        
    newImage = getImage(cap)
    photo = ImageTk.PhotoImage(newImage)
    imLabel.image = photo
    imLabel.configure(image=photo)
    print ("done updateing the gui \n")


#############################################################
# Description: returns the new directory's relative path
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################
def updateIMG():
    global mutex
    while True:
#        mutex.acquire()
        img = ImageTk.PhotoImage(getImage(cap))
        imLabel.configure(image = img)
        imLabel.image = img
 #       mutex.release()
        time.sleep(.05)

#############################################################
# Description: returns the new directory's relative path
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################
def moveTo(R,x,y,z,x_rot,y_rot,z_rot):
    q = transformations.quaternion_from_euler(x_rot, y_rot, z_rot, axes='sxyz')
    A = R.get_cartesian()
#    q = A[1]
    p = [x,y,z]
    pose_to_send = [p,q]
    R.set_cartesian(pose_to_send)
    time.sleep(1)

#############################################################
# Description: returns the new directory's relative path
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################
def moveTo_q(R,x,y,z,q0,q1,q2,q3):
    q = [q0,q1,q2,q3]
    p = [x,y,z]
    pose_to_send = [p,q]
    R.set_cartesian(pose_to_send)
    time.sleep(1)


#############################################################
# Description: returns the new directory's relative path
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################       
def processImage(R,i,cap,directory):
    global ImageId
    global ImageId_lock
 #   ImageId_lock.acquire()
    ImageId = ImageId + 1
  #  ImageId_lock.release()
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
    #to flush buffer 
    for i in xrange(0,20):
        print "caputre :"+str(i)+"\n" 
        ret, frame = cap.read();
    cv2.imwrite(imgFile,frame)
#    call(["./apriltags_demo",imgFile])
 
#############################################################
# Description: returns the new directory's relative path
#
# TODO REQUIERS
#
# TODO ENSURES 
#############################################################
def newLogFolder():
    if not os.path.exists('log_files'):
        os.makedirs('log_files')
    #creates a folder to store all of the images 
    directory = 'log_files/'+str(time.time())
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

##############################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
##############################################################
def logCurrentState(R,directory):
      station = -1
      i = -1
      processImage(R,i,cap,directory)
  
###############################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
###############################################################
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
            thisRow = row[0].split(',')
            print thisRow
            x = float(thisRow[0])
            y = float(thisRow[1])
            z = float(thisRow[2])
            q0 = float(thisRow[3])
            q1 = float(thisRow[4])
            q2 = float(thisRow[5])
            q3 = float(thisRow[6])
#            x_rot = float(thisRow[3])
#            y_rot = float(thisRow[4])
#            z_rot = float(thisRow[5])
#            station = int(thisRow[6])
            if(useRealRobot):
#                moveTo(R,x,y,z,x_rot,y_rot,z_rot);
                moveTo_q(R,x,y,z,q0,q1,q2,q3);
                block_while_moving(R)
            for i in xrange(0, num_pictures_per_location):
                processImage(R,i,cap,directory)
                
            
###########################################################
# TODO Description of function
#
# TODO REQUIERS
# 
# TODO ENSURES
###########################################################
def block_while_moving(R):
    while True:
        J0 =  R.get_joints()
        J1 =  R.get_joints()
        dj =  0.0
        for i in xrange(0,6):
            dj = dj + abs(J1[i] - J0[i])
        print "delta joints:"+str(dj) 
        if dj < 0.5:
            break;
    
    


############################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
############################################################          
def movePosition(R,changed_index,delta):
        global gui
        global cap
        position_curr = get_position_curr(R)
        position_curr[changed_index] += delta
                
        quad = position_curr[3:7]
        if(changed_index > 6):
            x_rot = position_curr[7]
            y_rot = position_curr[8]
            z_rot = position_curr[9]
            quad = transformations.quaternion_from_euler(x_rot, y_rot, z_rot, axes='sxyz')
            position_curr[3] = quad[0]
            position_curr[4] = quad[1]
            position_curr[5] = quad[2]
            position_curr[6] = quad[3]

        #change format of position_curr to what abb needs
        point = position_curr[0:3]
        pose_to_send = [point,quad]
        global mutex
        print pose_to_send
        R.set_cartesian(pose_to_send)
        block_while_moving(R)
        print "Done sending cartesian \n"
        global joint_labels
        global position_labels
        updateGUI(R,gui,cap,joint_labels,position_labels)

##########################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
##########################################################
def moveJoint(R,changed_index,delta):
        global gui
        global cap
        global joint_labels
        global position_labels
        axis_curr = R.get_joints();
        print axis_curr
	axis_curr[changed_index] += delta
        print "sending "+str(axis_curr)
        global mutex
        R.set_joints(axis_curr)
        print "Done sending joints \n"
        updateGUI(R,gui,cap,joint_labels,position_labels)


########################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
########################################################
def addJointControl(R,buttons,axis_curr,jNum):
	axis_label = Label(buttons,text="JOINT "+str(jNum))
	up_btn = Button(buttons,text="<",command=lambda:moveJoint(R,jNum-1,-10.0))
	curr_value  = Label(buttons,text=str(axis_curr[jNum-1])) 
        down_btn = Button(buttons,text=">",command=lambda:moveJoint(R,jNum-1,10.0))
	

	axis_label.grid(row=1,column=4*(jNum-1)+1)
	up_btn.grid(row=2,column=4*(jNum-1)+0)
	curr_value.grid(row=2,column=4*(jNum-1)+1)
	down_btn.grid(row=2,column=4*(jNum-1)+2)
        return curr_value

#######################################################
# TODO description of function 
#
# REQUIERS: 
#     R = #TODO
#     buttons = #TODO
#     position_curr = #TODO
#     name = #TODO
#     row = #TODO
#     col = #TODO
#     i = #TODO
#
# ENSURES:
#     return = label of the current value of the axis #TODO better description 
########################################################
def addPositionControl(R,buttons,name,row,col,i,delta):
	axis_label = Label(buttons,text=name)
	up_btn = Button(buttons,text="<",command=lambda:movePosition(R,i-1,delta))
	curr_value  = Label(buttons,text="0") 
	down_btn = Button(buttons,text=">",command=lambda:movePosition(R,i-1,-delta))

	axis_label.grid(row=row,column=4*(col-1)+1)
        up_btn.grid(row=row+1,column=4*(col-1)+0)
        curr_value.grid(row=row+1,column=4*(col-1)+1)
        down_btn.grid(row=row+1,column=4*(col-1)+2)
        return curr_value

#########################################################
# descriptiong: Go to home position, zero on all joints
#
# REQUIERS:
#
# ENSURES:
#
##########################################################
def MoveToZero(R):
    global gui
    global cap
    global joint_labels
    global position_labels
    R.set_joints([0,0,0,0,0,0])
    updateGUI(R,gui,cap,joint_labels,position_labels)    


##########################################################
# TODO description of function 
#
# REQUIERS:
# 
# ENSURES:
##########################################################
def drawGUI(gui,R,cap,axis_curr,directory):
        global imLabel 
        global joint_labels
        global position_labels
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
        joint_labels = [Label] * 6;
        position_labels = [Label]*10;
        buttons = Frame(gui)
	for jointNum in xrange(1,7):
		joint_labels[jointNum-1] = addJointControl(R,buttons,axis_curr,jointNum)


	position_labels[0] = addPositionControl(R,buttons,"X",3,1,1,50.0)
	position_labels[1] = addPositionControl(R,buttons,"Y",3,2,2,50.0)
	position_labels[2] = addPositionControl(R,buttons,"Z",3,3,3,50.0)
	position_labels[3] = addPositionControl(R,buttons,"q0",3,4,4,0.5)
	position_labels[4] = addPositionControl(R,buttons,"q1",3,5,5,0.5)
	position_labels[5] = addPositionControl(R,buttons,"q2",3,6,6,0.5)
	position_labels[6] = addPositionControl(R,buttons,"q3",3,7,7,0.5)
	position_labels[7] = addPositionControl(R,buttons,"roll",5,1,8,.125)
	position_labels[8] = addPositionControl(R,buttons,"pitch",5,2,9,.125)
	position_labels[9] = addPositionControl(R,buttons,"yaw",5,3,10,.125)
        buttons.grid()
	b = Button(buttons,text="Collect Data",command=lambda:collectData(R,directory))
	b.grid(row=7,column=0)

#        TODO does not work without global 
#        b1 = Button(buttons,text="new Log Folder",command=lambda:newLogFolder())
#	b1.grid(row=5,column=1)
        
        b2 = Button(buttons,text="log Current State",command=lambda:logCurrentState(R,directory))
	b2.grid(row=7,column=2)
        b3 = Button(buttons,text="zero",command=lambda:MoveToZero(R))
        b3.grid(row=7,column=3)
        #we want to get the actual values for the gui 
        updateGUI(R,gui,cap,joint_labels,position_labels)


#######################################################
# TODO Description of function 
#
# TODO REQUIERS
#
# TODO ENSURES 
#######################################################
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



	# should we test the system or use the real robot?
	# if false then do not try to connect to the real robot
	# if true then do try to connect to  to the real robot
	useRealRobot = True;  

	#number of pictures to take at each location
	num_pictures_per_location = 1;
 


	#connect to the robot 
	print "attempting to connect to the robot arm\n"
	if(useRealRobot):
            print "Attempting to connect to the actual robot, if the program hangs \
            make sure that the server for the robot is running.  You can also run \
            this program with a simulated robot \n"
	    R = abb.Robot(ip='192.168.125.1')
            #Can possibly hang here if can not connect to the robot #TODO quit if time out 
            camId = 0;
        else:
            R = abbSim.Robot()
            camId = 0;
	print "sucssfully connected to robot the robot arm\n"

	axis_curr = R.get_joints()
	cap = cv2.VideoCapture(camId)

        directory = newLogFolder();



        position_curr = get_position_curr(R)

        #seting up the gui 
	gui = Tk()
        drawGUI(gui,R,cap,axis_curr,directory)
#	otherButtons.grid(row=2,column=0) #side=TOP)
	mainloop()
        cap.release()
        cv2.destroyAllWindows()

main();
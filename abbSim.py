'''
 
Trevor Decker 

A simulator for the abb arm to test programs with the same interface as abb.py

'''

import json
import time
import inspect
from threading import Thread
from collections import deque
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Robot:
    internalJoints = [0,0,0,0,0,0]
    intrnalCartisian = [[0,0,0],[0,0,0,1]]

    def __init__(self,
                 ip = '0.0.0.0',
                 port_motion=0,
                 port_logger=0):
       
        self.delay = 0
        self.set_units('millimeters','degrees')
        self.set_tool()
        self.set_workobject()
        self.set_speed()
        self.set_zone()
     
    def connect_motion(self,remote):
       log.info('Attempting to connect to sim robot')
       log.info('connected to sim robot')
    
    def connect_logger(self,remote,maxlen=None):
       self.pose = deque(maxlen=maxlen)
       self.joints = deque(maxlen=maxlen)
       self.pose.append([data[2:5],data[5:]])
    
    def set_units(self, linear, angular):
        units_l = {'millimeters': 1.0,
                   'meters'     : 1000.0,
                   'inches'     : 25.4}
        units_a = {'degrees' : 1.0,
                   'radians' : 57.2957795}
        self.scale_linear = units_l[linear]
        self.scale_angle  = units_a[angular]
    
    def set_cartesian(self,pose):
       '''
       Executes a move immediately from the current pose,
       to 'pose', with units of millimeters.
       '''
       intrnalCartisian = pose;
       return True
    
    def set_joints(self,joints):
       '''
       Executes a move immediately, from current joint angles,
       to 'joints', in degrees.
       '''
       if len(joins) <> 6: return false
       internalJoints = self.joints;
       return True

    def get_cartesian(self):
       '''
       Returns the current pose of the robot, in millimeters
       '''
       return self.intrnalCartisian
       #TODO
    
    def get_joints(self):
       '''
       Returns the current angles of the robots joins, in degrees.
       '''
       return self.joints;
       #TODO
    
    
    def get_extenal_axis(self):
       pass
       #TODO continue porting from abb.py from this point on 

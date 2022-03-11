#!/usr/bin/env python3

import zmq
import rospy,math
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Pose, PoseWithCovariance, Twist
from tf.transformations import euler_from_quaternion

from turtlesim.msg import Pose
from sensor_msgs.msg import LaserScan
from math import pow, atan2, sqrt

import time

class Robot:
    """
    Listens for one of four inputs over TCP/IP comms (using zmq)
    Then applies that two actions for a robot using rospy
    """
    def __init__(self):    
        pass
    
    
    def listen(self):

        context = zmq.Context()
        # self.ctx = zmq.Context()
        socket = context.socket(zmq.SUB) # for UDP
        # socket = context.socket(zmq.REP)
        # socket.connect("tcp://*:5555")
        socket.connect("tcp://127.0.0.1:4441")
        socket.subscribe("")
        
        while True:
            command = socket.recv_string()       
            cmd = str(command)
            print("Command recieved: %s " % cmd)
            
            # self.sock.send_string("Confirmed %s " % cmd)
            
            if cmd in ['0', '1', '2', '3']:
                print('sending obey command')
                self.obey(cmd)
            elif cmd in ['i','o','k','j']:
                print('sending obey command')
                self.obey(cmd)


            time.sleep(1)

    
    def obey(self, command):
        
        # if the command is one of four commands
        if command=='0' or command=='i':

            # FWD
            cmd = 'tr'

        elif command=='1' or command=='o':

            # BKD    
            cmd = 'tl'
        
        elif command=='2' or command=='k':
            
            # RIGHT
            cmd = 'br'

        elif command=='3' or command=='l':
            
            # LEFT
            cmd = 'bl'

        else:
            raise Exception("Command not recognized >> obey( %s )?"% command)


        if cmd in ['tr', 'tl', 'br', 'bl']:
            self.move(cmd)

    
    def move(self, direction):
        
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rate = rospy.Rate(10)
        movCmd = Twist()
        speed = 0.2

        if direction=='tr':
            movCmd.linear.x = 1.0
            pub.publish(movCmd)

        elif direction=='tl':
            movCmd.linear.x = -1.0
            pub.publish(movCmd)

        elif direction=='br':
            movCmd.angular.z = 1.0
            pub.publish(movCmd)

        elif direction=='bl':
            movCmd.angular.z = -1.0
            pub.publish(movCmd)
        
        else:
            raise Exception("Command not recognized >> obey( %s )?"% command)
    ##################################################

    # ODOMETRY #########################################

    def getConvertedQData(self, oData : Odometry):

        qData = oData.pose.pose.orientation
        qDataList = [0,1,2,3]
        qDataList[0] = qData.x
        qDataList[1] = qData.y
        qDataList[2] = qData.z
        qDataList[3] = qData.w

        eData = euler_from_quaternion(qDataList)

        return eData

    def odomCallback(self, oData : Odometry):
        
        odomAsEuler = self.getConvertedQData(oData)
        self.yaw = radians2degrees(odomAsEuler[2])

    #### ROTATION CODE ########################################
    def __haltRotate(self):
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        outData = Twist()
        outData.angular.z = 0 # set angular speed to 0
        pub.publish(outData)

    def rotate45(self, direction):
        '''
        Rotates 45 degrees in the negative or positive direction
        '''
        if direction > 0:
            if self.debug:
                print("Attempting to rotate 45 degrees")
            self.rotate(45) # rotate left
        else:
            if self.debug:
                print("Attempting to rotate -45 degrees")
            self.rotate(-45) # rotate right

    def _convertOrientationTo360(self):
        '''
        Converts the Orientation from 180 , -180 to a full 360 degrees for readability
        '''
        toReturn = self.yaw

        if self.yaw < 0:
            toReturn = 360 + self.yaw
        return toReturn


    def rotate(self, desiredAngle):
        '''
        Rewritten rotate function that uses the ODOMETRY data
        @param desired angle: must be a value of no more than 180 degrees or -180 degrees
        '''
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        outData = Twist()
        angular_vel = degrees2radians(30.0)

        rate = rospy.Rate(10)
        
        # convert all values to 360 format ###

        currentOrientation = self._convertOrientationTo360()

        ######################################
        if desiredAngle == -45: # Turn right 
        
            current = self._convertOrientationTo360()
            distanceTraveled = 0

            turnTo = -45

            if self.debug:
                print("Turning right >> YAW: ", currentOrientation, "distanceTraveled: ", distanceTraveled)

            while distanceTraveled > turnTo:

                if currentOrientation == turnTo:
                    self.__haltRotate()

                currentOrientation = self._convertOrientationTo360()
                
                if self.debug:
                    print("Turning right >> YAW: ", current, "distanceTraveled: ", distanceTraveled)
                
                outData.angular.z = -abs(angular_vel) # for moving clockwise
                pub.publish(outData)
                rate.sleep()
                
                if self._convertOrientationTo360() > current:
                    # in event that YAW in 360 degrees is greater than current... from 0 to 360 ...
                    distanceTraveled += (360 - self._convertOrientationTo360()) - current

                else:
                    distanceTraveled += self._convertOrientationTo360() - current

                current = self._convertOrientationTo360()
            self.__haltRotate()      

        elif desiredAngle == 45: # turn left
            current = self._convertOrientationTo360()
            distanceTraveled = 0
            
            turnTo = 45

            if self.debug:
                print("Turning left >> YAW: ", current, "distanceTraveled: ", distanceTraveled)

            while distanceTraveled < turnTo:

                if currentOrientation == turnTo:
                    self.__haltRotate()

                currentOrientation = self._convertOrientationTo360()

                if self.debug:
                    print("Turning left >> YAW: ", current, "distanceTraveled: ", distanceTraveled)
                
                outData.angular.z = abs(angular_vel)
                pub.publish(outData)
                rate.sleep()

                if self._convertOrientationTo360() < current:
                    # crossed from 360 to 0
                    distanceTraveled += abs(360 + (self._convertOrientationTo360()) - current)
                    current = self._convertOrientationTo360()

                else:
                    distanceTraveled += abs(self._convertOrientationTo360() - current)
                    current = self._convertOrientationTo360()

            self.__haltRotate() 


    ##########################################################

#############################################

#####
def degrees2radians(angle):
    return angle * (math.pi/180.0)

def radians2degrees(angle):
    return math.degrees(angle)
####

# Run the machine
def run():
    myRobot = Robot()

    rospy.init_node('avatar', anonymous=True)

    # subscribe to known topics

    # rospy.Subscriber("/scan", LaserScan, myRobot.laserCallback)
    # rospy.Subscriber("/pose", Pose, myRobot.poseCallback)
    # rospy.Subscriber("/odom", Odometry, myRobot.odomCallback)


    myRobot.listen() # will run infintely

    rospy.spin()


if __name__ == "__main__":
    run()

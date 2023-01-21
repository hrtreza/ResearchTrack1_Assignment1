from __future__ import print_function
import time
from sr.robot import *
a_th = 2.0 
d_th = 0.4
#float: Threshold for the control of the orientation linear distance
R = Robot() #instance of the class Robot

def drive(speed, seconds):
"""
    Function for setting a linear velocity
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
"""
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
"""
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
"""
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def avoid_collision():
	 """
    find golden tokens and allocate the rotations to different zones
    to detect the distance of golden tokens respect to the robot

    """
  token_distances=[]
  token_rot_y=[]
  front_objects=[]
  left_objects=[]
  right_objects=[]
  crash = False
  for token in R.see():
    if token.dist < 3*d_th and token.info.marker_type is MARKER_TOKEN_GOLD:
      token_distances.append(token.dist)
      token_rot_y.append(token.rot_y)
      if -30*a_th < token.rot_y < 30*a_th:
        front_objects.append(token.dist)
      elif -60*a_th < token.rot_y < -30*a_th:
        right_objects.append(token.dist)
      elif 30*a_th < token.rot_y < 60*a_th:
        left_objects.append(token.dist)
  for dist in token_distances:
    if dist < 1.8*d_th:
     crash = True
  return front_objects , left_objects , right_objects , crash
  

def find_silver_token():
	    """
    Generate the rotation and distance form the Silver Token respect to the robot
    Retuens:
    1)distance respect to the robot
    2)rotation respect to the robot
    """
    dist=5
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and -60<token.rot_y<60:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==5:
	return -1, -1
    else:
   	return dist, rot_y
      
      
      
while 1:
 front_objects , left_objects , right_objects , crash = avoid_collision()
 silver_dist , silver_rot_y = find_silver_token()
 if crash == True:
  for nearest_token in front_objects:
    if nearest_token < 1.8*d_th:
      print("Ooopsss")
      if len(left_objects) >= len(right_objects):
        print("left lefttt")
        turn(-15, 0.5)
      else:
        print("Right righttt")
        turn(15, 0.5)
  drive(10,1)
 else:
    print("run")
    drive(18,1)
    if silver_dist==-1 or (-a_th)*30 >= silver_rot_y >= 30*a_th:  
	print("I don't see any token!!")
        continue
    elif silver_dist <d_th and -30*a_th <= silver_rot_y <= 30*a_th: # Condition for grabing the silver token if close enough
        print("Found it!")
        if R.grab():    # Uses the grab function fron Robot object
            print("Gotcha!")
	    turn(40, 2)
	    drive(5, 0.5)
	    R.release()
	    drive(-5,0.5)
	    turn(-40,2)
	else:
            print("Aww, I'm not close enough.")
    elif -a_th<= silver_rot_y <= a_th:
	print("Ah, that'll do.")
    elif silver_rot_y < -a_th:     # turn left if far from the token 
        print("Left a bit...")   
        turn(-5, 1)
    elif silver_rot_y > a_th:      # turn right if far from token
        print("Right a bit...")
        turn(+5, 1)
      
  
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
	

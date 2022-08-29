![Logo](https://github.com/LeonardoFerrisi/avatar/blob/main/avatar_logo.png)
# AVATAR
## An implementation for real-time Brain Computer Interfaces using ROS and Brainflow.

**A package for remotley controlling a robot with your mind. No really.**
______________________________________________________________________________________________________________________________

Instructions for usage:

:: Enabling virtual environment:
>> For Windows:
- source virtual_env/Scripts/activate
- pip install -r requirments.txt

>> For Ubuntu (tested on 16.x+): 
- source virtual_env_unix/bin/activate
- pip install -r requirments.txt

Main python library dependencies:

    - See requirements.txt... however heavily dependent on
    - Brainflow (https://brainflow.org/)
    - ZMQ (https://zeromq.org/)
    - pygame (https://www.pygame.org/)
    - numpy (https://numpy.org/)
    - ROS (and rospy of course) (https://www.ros.org/)

File Structure:
  
    |--avatar/
       |-- lib/
           |-- trinity/
               |-- client.py
               |-- sfpr.py
               |-- fbcca.py
       |-- src/
           |-- robo_ui.py
           |-- blink.py
           |-- ctrl.py
           |-- robot.py
        |--requirements.txt
        |--avatar_env/
        |--avatar_env_unix/

Recommended Hardware:

  - OpenBCI Cyton 8-Channel
  - Ultracortex MKIV Dry Electrodes
  - Turtlebot3 (fully charged!)
  - A brain (must be alive and safe inside someones head!)
  - Functioning Eyes (must also be snug inside someones eye sockets)
  - Two monitors, either connected to one or two computers


Operation:

    1. Navigate to /avatar/lib/trinity
    1a. Run client.py with a connected board 
    1b. Run sfpr.py after client.py has been run

    2. In a new terminal, run "roscore"
    2a. Open another new terminal, ssh into your robot
    2b. For turtlebot3, follow the tutorial here for connecting and enabling communication between host and robot: https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/
    2c. Once you have started and initialized your robot, run robot.py

    3. In a separate terminal (on a separate monitor if desired), run robo_ui.py

    4. Direct your attention to flashing squares and control the robot (with variable results, brain activity is NOISY)


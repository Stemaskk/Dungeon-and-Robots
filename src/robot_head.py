"""Robot head control: pan/tilt reactions at key story/game beats.

Owner: T
"""

from gretchen.robot import Robot
import time

def main():
    # Initalize & start robot
    #Device path to motor, camera
    #   Ubuntu/Linux  - motor: '/dev/grt_motor', camera: '/dev/grt_cam'
    #   Mac - motor: /dev/tty.usbserial-FT5WJ4JS', camera: '/dev/cu.usbserial-FT5WJ4JS' or 0
    #   Windows - motor: 'COM4', camera: 0
    robot = Robot('/dev/tty.usbserial-FT94ELKF', 0)
    robot.start()

def player_won_animation(robot, 
                         shake_angle=0.2,
                         head_down=-0.25,
                         repeats=3,
                         pause=0.5,
                         ):
     robot.move(0, head_down)
     time.sleep(0.5)

     #small shaking movements to indicate disappointment
     for _ in range(repeats):
         robot.move(shake_angle, head_down)
         time.sleep(pause)

         robot.move(0, head_down)
         time.sleep(0.05)

         robot.move(-shake_angle, head_down)
         time.sleep(pause)

         robot.move(0, head_down)
         time.sleep(0.05)

def player_lost_animation(robot,
                          look_up=0.2,
                          nod_depth=0.12,
                          repeats=3,
                          pause=0.5
                          ):
    
    #calculate lower position for nodding
    lower_position = look_up - nod_depth
    
    robot.move(0, look_up)
    time.sleep(0.5)

    #small nodding movements to indicate victory
    for _ in range(repeats):
        robot.move(0, lower_position)
        time.sleep(pause)

        robot.move(0, look_up)
        time.sleep(pause)
    




"""Robot head control: pan/tilt reactions at key story/game beats.

Owner: T
"""
import time

def react(robot, outcome):
    if outcome == "won":
        player_won_animation(robot)
    elif outcome == "lost":
        player_lost_animation(robot)

def player_won_animation(robot, 
                         shake_angle=0.2,
                         head_down=-0.25,
                         repeats=3,
                         pause=0.25,
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
     robot.move(0,0)
     time.sleep(0.5)

def player_lost_animation(robot,
                          look_up=0.4,
                          nod_depth=0.2,
                          repeats=3,
                          pause=0.25
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
    robot.move(0,0)
    time.sleep(0.5)
    




#################################
# YOU SHOULD NOT EDIT THIS FILE #
#################################

# Import some external libraries
import time
import numpy as np
import pyglet

# Imports from this project
import constants
from environment import Environment
from robot import Robot
from graphics import Graphics


# Set the numpy random seed
seed = int(time.time())
np.random.seed(seed)
# Create an environment, which is the physical world the robot moves around in
environment = Environment()
state = environment.reset()
# Create a robot, which is the "brain" controlling the robot
robot = Robot()
# Create a graphics object, which controls what and where objects should be rendered on the window
graphics = Graphics()
# Create a window on the screen
window = graphics.create_window()
# Set the current mode
mode = 'waiting'


# Function that is called at a regular interval and is used to trigger the robot to plan or execute actions
def update(dt):
    global mode
    global state
    # If the robot is currently waiting, then start planning
    if mode == 'waiting':
        mode = 'demonstrating'
    # If the robot is currently planning, then compute the plan
    elif mode == 'demonstrating':
        demonstration_states, demonstration_actions = environment.get_demonstrations()
        robot.train_on_demonstrations(demonstration_states, demonstration_actions)
        mode = 'acting'
    # If the robot is currently acting, then execute the next action in the plan
    elif mode == 'acting':
        done, action = robot.get_next_action(state)
        next_state = environment.step(action)
        state = next_state
        if done:
            state = environment.reset()
            mode = 'waiting'


# Function that is called at a regular interval to draw the environment and visualisation on the window
@window.event
def on_draw():
    graphics.draw(environment, robot)


# Set the rate at which the update() function is called
# (Note that the rate at which on_draw() is not set by this)
pyglet.clock.schedule_interval(update, 1/constants.UPDATE_RATE)

# Run the application, which will start calling update() and on_draw()
pyglet.app.run()

#################################
# YOU SHOULD NOT EDIT THIS FILE #
#################################

# Size of the world, i.e. the coordinate frame in which the robot's state is defined
WORLD_SIZE = 100

# Attributes for the robot
ROBOT_NUM_LINKS = 3
ROBOT_LINK_WIDTH = 3
ROBOT_LINK_LENGTHS = (20, 15, 10)
ROBOT_JOINT_RADIUS = 2
ROBOT_EEF_RADIUS = 3
ROBOT_JOINT_COLOUR = (200, 200, 200, 255)  # Colours from 0 -> 255
ROBOT_LINK_COLOUR = (150, 150, 150, 255)  # Colours from 0 -> 255
ROBOT_EEF_COLOUR = (150, 150, 255, 255)  # Colours from 0 -> 255

# Attributes for the goal
GOAL_RADIUS = 2
GOAL_COLOUR = (100, 200, 100, 255)

# Attributes for the obstacles
OBSTACLE_COLOUR = (150, 50, 50, 255)

# Attributes for the boundary
BOUNDARY_WIDTH = 0.5
BOUNDARY_COLOUR = (100, 100, 100, 255)

# Attributes for the environment background
ENVIRONMENT_COLOUR = (0, 0, 0, 255)
BACKGROUND_COLOUR_GL = (0, 0, 0, 1)

# The number of times per second the state of the environment is updated
UPDATE_RATE = 10

# The maximum action magnitude the robot can execute in each action dimension
ROBOT_MAX_ACTION = 5



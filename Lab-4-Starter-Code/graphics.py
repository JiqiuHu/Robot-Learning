#################################
# YOU SHOULD NOT EDIT THIS FILE #
#################################

# Import some external libraries
import numpy as np
import pyglet

# Imports from this project
import constants
import configuration


# Function to convert from world space to window space
def world_to_window(world_pos):
    window_pos = int((world_pos / constants.WORLD_SIZE) * configuration.WINDOW_SIZE)
    return window_pos


# The Graphics class is used to decide what and where to draw on the window
class Graphics:

    def __init__(self):
        self.window = None
        self.middle_space = int(0.01 * configuration.WINDOW_SIZE)
        self.top_space = int(0.05 * configuration.WINDOW_SIZE)
        self.visualisation_iteration_num = 0
        self.num_visualisation_steps = 0

    # Function to create a new pyglet window
    def create_window(self):
        # Create a new window
        window_width = 2 * configuration.WINDOW_SIZE + self.middle_space
        window_height = configuration.WINDOW_SIZE + self.top_space
        self.window = pyglet.window.Window(width=window_width, height=window_height)
        # Set the background colour
        pyglet.gl.glClearColor(*constants.BACKGROUND_COLOUR_GL)
        self.window.clear()
        # Return the window to the main script
        return self.window

    # Function to draw the environment and visualisations to the screen
    def draw(self, environment, robot):
        # Clear the entire window
        self.window.clear()
        # Draw the titles
        self.draw_titles()
        # LIVE ENVIRONMENT (left)
        x_left = 0
        # Draw the environment
        self.draw_environment(environment, x_left=x_left)
        self.draw_boundary(x_left=x_left)
        # Draw the robot
        self.draw_robot(environment.robot_current_state, environment, x_left=x_left)
        # DEMONSTRATION VISUALISATION (right)
        x_left += configuration.WINDOW_SIZE + self.middle_space
        # Draw the environment
        self.draw_environment(environment, x_left=x_left)
        self.draw_boundary(x_left=x_left)
        # Draw the robot
        self.draw_robot(environment.robot_init_state, environment, x_left=x_left)
        # Draw the demonstrations
        self.draw_demonstrations(environment, x_left=x_left)

    # Function to draw the titles for the left-hand and right-hand sides
    def draw_titles(self):
        font_size = configuration.WINDOW_SIZE * 0.03
        text_x = int(0.5 * configuration.WINDOW_SIZE)
        text_y = configuration.WINDOW_SIZE
        label = pyglet.text.Label('Live Environment', font_name='Arial', font_size=font_size, x=text_x, y=text_y, anchor_x='center', anchor_y='bottom')
        label.draw()
        x_left = configuration.WINDOW_SIZE + self.middle_space
        text_x = int(x_left + 0.5 * configuration.WINDOW_SIZE)
        text_y = configuration.WINDOW_SIZE
        label = pyglet.text.Label('Demonstrations Visualisation', font_name='Arial', font_size=font_size, x=text_x, y=text_y, anchor_x='center', anchor_y='bottom')
        label.draw()

    # Function to draw the environment, i.e. any obstacles and the goal
    def draw_environment(self, environment, x_left):
        self.draw_goal(environment, x_left)

    def draw_robot(self, state, environment, x_left):
        # Calculate the link positions
        link1_position, link2_position, link3_position = environment.calculate_link_positions(state)
        # Convert these from world to window coordinates
        link1_x1_window = x_left + world_to_window(link1_position[0])
        link1_y1_window = world_to_window(link1_position[1])
        link1_x2_window = x_left + world_to_window(link1_position[2])
        link1_y2_window = world_to_window(link1_position[3])
        link2_x1_window = x_left + world_to_window(link2_position[0])
        link2_y1_window = world_to_window(link2_position[1])
        link2_x2_window = x_left + world_to_window(link2_position[2])
        link2_y2_window = world_to_window(link2_position[3])
        link3_x1_window = x_left + world_to_window(link3_position[0])
        link3_y1_window = world_to_window(link3_position[1])
        link3_x2_window = x_left + world_to_window(link3_position[2])
        link3_y2_window = world_to_window(link3_position[3])
        # Draw the links
        link1_width = world_to_window(constants.ROBOT_LINK_WIDTH)
        link1_shape = pyglet.shapes.Line(x=link1_x1_window, y=link1_y1_window, x2=link1_x2_window, y2=link1_y2_window, width=link1_width, color=constants.ROBOT_LINK_COLOUR)
        link1_shape.draw()
        link2_width = world_to_window(constants.ROBOT_LINK_WIDTH)
        link2_shape = pyglet.shapes.Line(x=link2_x1_window, y=link2_y1_window, x2=link2_x2_window, y2=link2_y2_window, width=link2_width, color=constants.ROBOT_LINK_COLOUR)
        link2_shape.draw()
        link3_width = world_to_window(constants.ROBOT_LINK_WIDTH)
        link3_shape = pyglet.shapes.Line(x=link3_x1_window, y=link3_y1_window, x2=link3_x2_window, y2=link3_y2_window, width=link3_width, color=constants.ROBOT_LINK_COLOUR)
        link3_shape.draw()
        # Draw the joints
        joint1_radius = world_to_window(constants.ROBOT_JOINT_RADIUS)
        joint1_shape = pyglet.shapes.Circle(x=link1_x1_window, y=link1_y1_window, radius=joint1_radius, color=constants.ROBOT_JOINT_COLOUR)
        joint1_shape.draw()
        joint2_radius = world_to_window(constants.ROBOT_JOINT_RADIUS)
        joint2_shape = pyglet.shapes.Circle(x=link2_x1_window, y=link2_y1_window, radius=joint2_radius, color=constants.ROBOT_JOINT_COLOUR)
        joint2_shape.draw()
        joint3_radius = world_to_window(constants.ROBOT_JOINT_RADIUS)
        joint3_shape = pyglet.shapes.Circle(x=link3_x1_window, y=link3_y1_window, radius=joint3_radius, color=constants.ROBOT_JOINT_COLOUR)
        joint3_shape.draw()
        # Draw the eef
        eef_radius = world_to_window(constants.ROBOT_EEF_RADIUS)
        eef_shape = pyglet.shapes.Circle(x=link3_x2_window, y=link3_y2_window, radius=eef_radius, color=constants.ROBOT_EEF_COLOUR)
        eef_shape.draw()

    # Function to draw the environment's boundary
    def draw_boundary(self, x_left):
        # Left boundary
        x = x_left
        y = 0
        width = world_to_window(constants.BOUNDARY_WIDTH)
        height = world_to_window(100)
        left_boundary_shape = pyglet.shapes.Rectangle(x, y, width, height, constants.BOUNDARY_COLOUR)
        left_boundary_shape.draw()
        # Right boundary
        x = x_left + world_to_window(100 - constants.BOUNDARY_WIDTH)
        y = 0
        width = world_to_window(constants.BOUNDARY_WIDTH)
        height = world_to_window(100)
        left_boundary_shape = pyglet.shapes.Rectangle(x, y, width, height, constants.BOUNDARY_COLOUR)
        left_boundary_shape.draw()
        # Top boundary
        x = x_left
        y = world_to_window(100 - constants.BOUNDARY_WIDTH)
        width = world_to_window(100)
        height = world_to_window(constants.BOUNDARY_WIDTH)
        left_boundary_shape = pyglet.shapes.Rectangle(x, y, width, height, constants.BOUNDARY_COLOUR)
        left_boundary_shape.draw()
        # Bottom boundary
        x = x_left
        y = 0
        width = world_to_window(100)
        height = world_to_window(constants.BOUNDARY_WIDTH)
        left_boundary_shape = pyglet.shapes.Rectangle(x, y, width, height, constants.BOUNDARY_COLOUR)
        left_boundary_shape.draw()

    # Function to draw the goal
    def draw_goal(self, environment, x_left):
        if environment.goal_state is None:
            return
        goal_x_window = x_left + world_to_window(environment.goal_state[0])
        goal_y_window = world_to_window(environment.goal_state[1])
        goal_radius = world_to_window(constants.GOAL_RADIUS)
        goal_colour = constants.GOAL_COLOUR
        goal_shape = pyglet.shapes.Circle(x=goal_x_window, y=goal_y_window, radius=goal_radius, color=goal_colour)
        goal_shape.draw()

    # Function to draw the demonstrations on the right side of the window
    def draw_demonstrations(self, environment, x_left):
        batch = pyglet.graphics.Batch()
        shape_list = []
        num_demos = len(environment.demonstration_eef_paths)
        for demo_num in range(num_demos):
            eef_path = environment.demonstration_eef_paths[demo_num]
            num_states = len(eef_path)
            prev_state = eef_path[0]
            prev_state_x_window = x_left + world_to_window(prev_state[0])
            prev_state_y_window = world_to_window(prev_state[1])
            for state_num in range(1, num_states):
                next_state = eef_path[state_num]
                next_state_x_window = x_left + world_to_window(next_state[0])
                next_state_y_window = world_to_window(next_state[1])
                line_shape = pyglet.shapes.Line(x=prev_state_x_window, y=prev_state_y_window, x2=next_state_x_window, y2=next_state_y_window, width=3, color=(255, 255, 255, 255), batch=batch)
                shape_list.append(line_shape)
                prev_state_x_window = next_state_x_window
                prev_state_y_window = next_state_y_window
        batch.draw()

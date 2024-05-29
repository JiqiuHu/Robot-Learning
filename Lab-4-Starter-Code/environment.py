#################################
# YOU SHOULD NOT EDIT THIS FILE #
#################################

# Import some external libraries
import numpy as np

# Imports from this project
import constants
import configuration


# The Environment class represents the physical environment that the robot moves around in
class Environment:

    def __init__(self):
        self.robot_init_state = np.array([90, 0.0, 0.0])
        self.robot_current_state = self.robot_init_state
        self.robot_base_position = np.array([50, 50])
        self.goal_state = np.random.uniform([0.6 * constants.WORLD_SIZE, 0.2 * constants.WORLD_SIZE], [0.7 * constants.WORLD_SIZE, 0.7 * constants.WORLD_SIZE], 2)
        self.demonstration_eef_paths = []

    # Function to execute an action in the environment, and update the robot's state
    def step(self, action):
        # Calculate the next state using the environment dynamics
        next_state = self.robot_current_state + action
        self.robot_current_state = next_state
        return self.robot_current_state

    # Function to reset the environment, which moves the robot back to its initial state
    def reset(self):
        self.robot_current_state = self.robot_init_state
        self.demonstration_eef_paths = []
        return self.robot_current_state

    def get_demonstrations(self):
        demonstration_states = np.zeros([configuration.NUM_DEMONSTRATIONS, configuration.CEM_PATH_LENGTH, 3], dtype=np.float32)
        demonstration_actions = np.zeros([configuration.NUM_DEMONSTRATIONS, configuration.CEM_PATH_LENGTH, 3], dtype=np.float32)
        for demo_num in range(configuration.NUM_DEMONSTRATIONS):
            # planning_actions is the full set of actions that are sampled
            planning_actions = np.zeros([configuration.CEM_NUM_ITERATIONS, configuration.CEM_NUM_PATHS, configuration.CEM_PATH_LENGTH, 3], dtype=np.float32)
            # planning_paths is the full set of paths (one path is a sequence of states) that are evaluated
            planning_paths = np.zeros([configuration.CEM_NUM_ITERATIONS, configuration.CEM_NUM_PATHS, configuration.CEM_PATH_LENGTH, 3], dtype=np.float32)
            # planning_path_rewards is the full set of path rewards that are calculated
            planning_path_rewards = np.zeros([configuration.CEM_NUM_ITERATIONS, configuration.CEM_NUM_PATHS])
            # planning_mean_actions is the full set of mean action sequences that are calculated at the end of each iteration (one sequence per iteration)
            planning_mean_actions = np.zeros([configuration.CEM_NUM_ITERATIONS, configuration.CEM_PATH_LENGTH, 3], dtype=np.float32)
            # Loop over the iterations
            robot_current_state = self.robot_init_state
            for iteration_num in range(configuration.CEM_NUM_ITERATIONS):
                for path_num in range(configuration.CEM_NUM_PATHS):
                    planning_state = np.copy(robot_current_state)
                    for step_num in range(configuration.CEM_PATH_LENGTH):
                        if iteration_num == 0:
                            action = np.random.uniform(-constants.ROBOT_MAX_ACTION, constants.ROBOT_MAX_ACTION, 3)
                        else:
                            action = np.random.normal(best_paths_action_mean[step_num], best_paths_action_std_dev[step_num])
                        planning_actions[iteration_num, path_num, step_num] = action
                        next_state = self.dynamics_model(planning_state, action)
                        planning_paths[iteration_num, path_num, step_num] = next_state
                        planning_state = next_state
                    path_reward = self.compute_reward(planning_paths[iteration_num, path_num])
                    planning_path_rewards[iteration_num, path_num] = path_reward
                sorted_path_rewards = planning_path_rewards[iteration_num].copy()
                sorted_path_costs = np.argsort(sorted_path_rewards)
                indices_best_paths = sorted_path_costs[-configuration.CEM_NUM_ELITES:]
                best_paths_action_mean = np.mean(planning_actions[iteration_num, indices_best_paths], axis=0)
                best_paths_action_std_dev = np.std(planning_actions[iteration_num, indices_best_paths], axis=0)
                planning_mean_actions[iteration_num] = best_paths_action_mean
            # Calculate the index of the best path
            index_best_path = np.argmax(planning_path_rewards[-1])
            # Set the planned path (i.e. the best path) to be the path whose index is index_best_path
            planned_path = planning_paths[-1, index_best_path]
            demonstration_states[demo_num] = planned_path
            # Set the planned actions (i.e. the best action sequence) to be the action sequence whose index is index_best_path
            planned_actions = planning_actions[-1, index_best_path]
            demonstration_actions[demo_num] = planned_actions
        # Create the 2D eef path from the 3D path of joint angles
        self.demonstration_eef_paths = np.zeros([configuration.NUM_DEMONSTRATIONS, configuration.CEM_PATH_LENGTH, 2])
        for demo_num in range(configuration.NUM_DEMONSTRATIONS):
            path = demonstration_states[demo_num]
            num_states = len(path)
            for state_num in range(num_states):
                eef_position = self.calculate_eef_position(path[state_num])
                self.demonstration_eef_paths[demo_num, state_num] = eef_position
        return demonstration_states, demonstration_actions

    def dynamics_model(self, state, action):
        next_state = state + action
        return next_state

    def compute_reward(self, path):
        eef_position = self.calculate_eef_position(path[-1])
        distance = np.linalg.norm(eef_position - self.goal_state)
        reward = -distance
        return reward

    def calculate_link_positions(self, state):
        # Link 1
        link1_x1 = self.robot_base_position[0]
        link1_y1 = self.robot_base_position[1]
        link1_x2 = link1_x1 + constants.ROBOT_LINK_LENGTHS[0] * np.cos(np.deg2rad(state[0]))
        link1_y2 = link1_y1 + constants.ROBOT_LINK_LENGTHS[0] * np.sin(np.deg2rad(state[0]))
        # Link 2
        link2_x1 = link1_x2
        link2_y1 = link1_y2
        link2_x2 = link2_x1 + constants.ROBOT_LINK_LENGTHS[1] * np.cos(np.deg2rad(state[0] + state[1]))
        link2_y2 = link2_y1 + constants.ROBOT_LINK_LENGTHS[1] * np.sin(np.deg2rad(state[0] + state[1]))
        # Link 3
        link3_x1 = link2_x2
        link3_y1 = link2_y2
        link3_x2 = link3_x1 + constants.ROBOT_LINK_LENGTHS[2] * np.cos(np.deg2rad(state[0] + state[1] + state[2]))
        link3_y2 = link3_y1 + constants.ROBOT_LINK_LENGTHS[2] * np.sin(np.deg2rad(state[0] + state[1] + state[2]))
        # Return these link positions (the end of each link)
        return (link1_x1, link1_y1, link1_x2, link1_y2), (link2_x1, link2_y1, link2_x2, link2_y2), (link3_x1, link3_y1, link3_x2, link3_y2)

    def calculate_eef_position(self, state):
        _, _, link3_pos = self.calculate_link_positions(state)
        eef_position = np.array([link3_pos[2], link3_pos[3]])
        return eef_position

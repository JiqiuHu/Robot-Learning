##########################
# YOU CAN EDIT THIS FILE #
##########################

# Import some external libraries
import numpy as np
import torch
from matplotlib import pyplot as plt
import random
# Imports from thi project
import constants
import configuration


# The Robot class is the "brain" of the robot, and is used to decide what action to execute in the environment.
class Robot:

    def __init__(self):
        self.dynamics_model_network = Network()


    def train_on_demonstrations(self, demonstration_states, demonstration_actions):
        # TODO
        # Create the optimiser
        optimiser = torch.optim.Adam(self.dynamics_model_network.parameters(), lr=0.01)

        # Create lists to store the losses and epochs
        losses = []
        iterations = []

        # Create a graph which will show the loss as a function of the number of training iterations
        fig, ax = plt.subplots()
        ax.set(xlabel='Iteration', ylabel='Loss', title='Loss Curve for Cross Entropy')

        # Loop over training iterations
        for training_iteration in range(10):
            # sample batch
            data = torch.tensor(demonstration_states, dtype=torch.float32)
            label = torch.tensor(demonstration_actions, dtype=torch.float32)

            # Set all the gradients stored in the optimiser to zero.
            optimiser.zero_grad()
            # Do a forward pass of the network using the inputs batch
            state_tensor = torch.tensor(state_batch[:, :, 0], dtype=torch.float32)
            action_tensor = torch.tensor(action_batch[:, :, 0], dtype=torch.float32)
            # Make a prediction with the neural network
            network_input = torch.cat((state_tensor, action_tensor), dim=-1)
            network_input = torch.unsqueeze(network_input, 0)
            network_prediction = self.dynamics_model_network.forward(network_input)[0]
            # Compute the loss based on the label's batch
            loss = torch.nn.MSELoss()(network_prediction, label_data)
            # Compute the gradients based on this loss,
            # i.e. the gradients of the loss with respect to the network parameters.
            loss.backward()
            # Take one gradient step to update the network
            optimiser.step()
            # Get the loss as a scalar value
            loss_value = loss.item()
            # Print out this loss
            # print('Iteration ' + str(training_iteration) + ', Loss = ' + str(loss_value))
            # Store this loss in the list
            losses.append(loss_value)
            # Update the list of iterations
            iterations.append(training_iteration)
        ax.plot(iterations, losses, color='blue')
        plt.yscale('log')
        plt.show()
        fig.savefig("loss_curve.png")

    # Function to get the next action in the plan
    def get_next_action(self, state):
        # TODO
        random_action = np.random.uniform(-constants.ROBOT_MAX_ACTION, constants.ROBOT_MAX_ACTION, 3)
        return False, random_action

class Network(torch.nn.Module):

    # The class initialisation function.
    def __init__(self):
        # Call the initialisation function of the parent class.
        super(Network, self).__init__()
        # Define the network layers. This example network has two hidden layers, each with 10 units.
        self.layer_1 = torch.nn.Linear(in_features=3, out_features=10, dtype=torch.float32)
        self.layer_2 = torch.nn.Linear(in_features=10, out_features=10, dtype=torch.float32)
        self.output_layer = torch.nn.Linear(in_features=10, out_features=3, dtype=torch.float32)

    # Function which sends some input data through the network and returns the network's output.
    def forward(self, input):
        layer_1_output = torch.nn.functional.relu(self.layer_1(input))
        layer_2_output = torch.nn.functional.relu(self.layer_2(layer_1_output))
        output = self.output_layer(layer_2_output)
        return output

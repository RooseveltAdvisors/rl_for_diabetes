"""
OPENAI gym environment for the Cambridge/Hovorka model
This is the base class for the Hovorka models.
    - Actions runs for a longer interval (default 30 mins)
    to get closer to a markov decision process.
    - The model includes meals
    - Default 34 dim observation space (30 min BG and last four actions)
    - Default action space 0 to 50 mU/min of insulin
    - Rendering disabled by default
    - Initialization and reset: Random initialization and no meals!
"""

import logging
import gym
from gym import spaces

import numpy as np

# Plotting for the rendering
# import matplotlib.pyplot as plt

# Cambridge simulator
from gym.envs.cambridge_model.cambridge_model import cambridge_model, cambridge_model_tuple, cambridge_parameters
from gym.envs.cambridge_model.subject import subject
from gym.envs.cambridge_model.reward_function import calculate_reward

# ODE solver stuff
from scipy.integrate import ode
from scipy.optimize import fsolve

logger = logging.getLogger(__name__)

class CambridgeBase(gym.Env):
    # TODO: fix metadata??
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        """
        Initializing the simulation environment.
        """

        # Action space
        self.previous_action = 0

        # State space
        self.observation_space = spaces.Box(0, 500, (34,))
        # self.observation_space = spaces.Box(0, 500, 1)

        self.bolus = 0

        ## Loading variable parameters
        # meal_times, meal_amounts, reward_flag, bg_init_flag = self._update_parameters()
        reward_flag, bg_init_flag = self._update_parameters()

        # Action space
        # ====================================
        # Normalized action space!!
        # ====================================
        # self.action_space = spaces.Box(0, 50, (1,))
        self.action_space = spaces.Box(-1, 1, (1,))

        # Initial basal -- this rate dictates the initial BG value

        if bg_init_flag == 'random':
            self.init_basal = np.random.choice(np.linspace(4, 6.428, 50))
        elif bg_init_flag == 'fixed':
            self.init_basal = 6

        # Flag for manually resetting the init
        self.reset_basal_manually = None

        # self.seed()
        self.viewer = None

        # ==========================================
        # Setting up the cambridge simulator
        # ==========================================

        # Patient parameters -- sub_1() means virtual patient #1
        # P = subject(1)
        # P = subject(2)
        # P = subject(3)
        P = subject(4)
        # P = subject(5)
        # P = subject(6)

        self.P = P

        # Initial values for parameters
        initial_pars = (self.init_basal, 0, P)

        # Initial value
        X0 = fsolve(cambridge_model_tuple, np.zeros(11), args=initial_pars)
        self.X0 = X0

        # Simulation setup
        self.integrator = ode(cambridge_model)
        self.integrator.set_integrator('vode', method='bdf', order=5)
        self.integrator.set_initial_value(X0, 0)

        # Simulation time in minutes
        self.simulation_time = 30

        # State is BG, simulation_state is parameters of hovorka model
        initial_bg = X0[-1] * P[12]
        initial_insulin = np.zeros(4)
        self.state = np.concatenate([np.repeat(initial_bg, self.simulation_time), initial_insulin])

        self.simulation_state = X0

        # Keeping track of entire blood glucose level for each episode
        self.bg_history = []
        self.insulin_history = initial_insulin

        # Meal setup
        # ====================

        # meal_times = [round(np.random.uniform(690,750))]
        # meal_amounts = [round(np.random.uniform(50,60))]

        meal_times = [0]
        meal_amounts = [0]

        # meal_times = [round(np.random.uniform(330,390)), round(np.random.uniform(690,750)), round(np.random.uniform(1050,1110))]
        # meal_amounts = [round(np.random.uniform(70,80)), round(np.random.uniform(50,60)), round(np.random.uniform(50,60))]

        # Adding guessed meal amount
        # guessed_meal_amount = [round(np.random.uniform(meal_amounts[0]-20, meal_amounts[0]+20)), \
        #                       round(np.random.uniform(meal_amounts[1]-20, meal_amounts[1]+20)), round(np.random.uniform(meal_amounts[2]-20, meal_amounts[2]+20))]

        eating_time = 30
        premeal_bolus_time = 15

        # Meals indicates the number of carbs taken at time t
        meals = np.zeros(1440)

        # 'meal_indicator' indicates time of bolus - default 30 minutes before meal
        meal_indicator = np.zeros(1440)

        for i in range(len(meal_times)):
            meals[meal_times[i] : meal_times[i] + eating_time] = meal_amounts[i]/eating_time * 1000 /180
            meal_indicator[meal_times[i]-premeal_bolus_time:meal_times[i]] = meal_amounts[i] * 1000 / 180

            # Changing to guessed meal amount
            # meal_indicator[meal_times[i]-premeal_bolus_time] = guessed_meal_amount[i] * 1000 / 180

        # TODO: Clean up these
        self.meals = meals
        self.meal_indicator = meal_indicator
        self.eating_time = eating_time
        self.premeal_bolus_time = premeal_bolus_time

        # Counter for number of iterations
        self.num_iters = 0

        # If blood glucose is less than zero, the simulator is out of bounds.
        self.bg_threshold_low = 0
        self.bg_threshold_high = 500

        # TODO: This number is arbitrary
        self.max_iter = 1440

        # Reward flag
        self.reward_flag = reward_flag

        self.steps_beyond_done = None

    def _seed():
        return None

    def _update_parameters(self):
        ''' Update parameters of model,
        this is only used for inherited classes'''

        # meal_times = [0]
        # meal_amounts = [0]
        reward_flag = 'gaussian'
        bg_init_flag = 'random'
        # action_space = spaces.box(0, 30, 1)

        # return meal_times, meal_amounts, reward_flag, bg_init_flag
        return reward_flag, bg_init_flag

    def step(self, action):
        """
        Take action. In the diabetes simulation this means increase, decrease or do nothing
        to the insulin to carb ratio (bolus).
        """
        if action > self.action_space.high:
            action = self.action_space.high
        elif action < self.action_space.low:
            action = self.action_space.low

        # assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        # Converting scaled action
        ub = 50
        lb = 0
        action = lb + (action + 1) * .5 * (ub - lb)

        self.integrator.set_initial_value(self.simulation_state, self.num_iters)

        bg = []
        insulin = []
        # ==========================
        # Integration loop
        # ==========================
        for i in range(self.simulation_time):

            # ===============================================
            # Solving one step of the Hovorka model
            # ===============================================

            insulin_rate = action + (self.meal_indicator[self.num_iters] * self.bolus)/self.premeal_bolus_time
            self.integrator.set_f_params(insulin_rate, self.meals[self.num_iters], self.P)

            self.integrator.integrate(self.integrator.t + 1)

            self.num_iters += 1
            bg.append(self.integrator.y[-1] * self.P[12])
            # insulin.append(self.integrator.y[6])
            insulin.append(insulin_rate)

        # Updating environment parameters
        self.simulation_state = self.integrator.y

        # Recording bg history for plotting
        self.bg_history = np.concatenate([self.bg_history, bg])

        # adding average insulin of last 30 minutes
        self.insulin_history = np.concatenate([self.insulin_history, np.atleast_1d(np.mean(insulin))])

        # Updating state

        self.state = np.concatenate([bg, list(reversed(self.insulin_history[-4:]))])

        #Set environment done = True if blood_glucose_level is negative
        done = 0

        if (np.max(bg) > self.bg_threshold_high or np.max(bg) < self.bg_threshold_low):
            done = 1

        if self.num_iters > self.max_iter:
            done = 1

        done = bool(done)

        # ====================================================================================
        # Calculate Reward  (and give error if action is taken after terminal state)
        # ====================================================================================

        if not done:
            if self.reward_flag != 'gaussian_with_insulin':
                reward = calculate_reward(np.array(bg), self.reward_flag, 108)
            else:
                reward = calculate_reward(np.array(bg), 'gaussian_with_insulin', 108, action)

        elif self.steps_beyond_done is None:
            # Blood glucose below zero -- simulation out of bounds
            self.steps_beyond_done = 0
            # reward = 0.0
            # reward = -1000
            if self.reward_flag != 'gaussian_with_insulin':
                reward = calculate_reward(np.array(bg), self.reward_flag, 108)
            else:
                reward = calculate_reward(np.array(bg), 'gaussian_with_insulin', 108, action)
        else:
            if self.steps_beyond_done == 0:
                logger.warning("You are calling 'step()' even though this environment has already returned done = True. You should always call 'reset()' once you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = -1000

        self.previous_action = action

        return np.array(self.state), np.mean(reward), done, {}


    def reset(self):
        #TODO: Insert init code here!

        # re init -- in case the init basal has been changed
        if self.reset_basal_manually is None:
            self.init_basal = np.random.choice(np.linspace(4, 6.428, 50))
            # self.init_basal = 6
        else:
            self.init_basal = self.reset_basal_manually

        P = self.P
        initial_pars = (self.init_basal, 0, P)

        X0 = fsolve(cambridge_model_tuple, np.zeros(11), args=initial_pars)
        self.X0 = X0
        self.integrator.set_initial_value(self.X0, 0)

        # State is BG, simulation_state is parameters of hovorka model
        initial_bg = X0[-1] * P[12]
        initial_insulin = np.zeros(4)
        self.state = np.concatenate([np.repeat(initial_bg, self.simulation_time), initial_insulin])

        self.simulation_state = X0
        self.bg_history = []
        self.insulin_history = initial_insulin

        self.num_iters = 0


        # changing observation space if simulation time is changed
        if self.simulation_time != 30:
            self.observation_space = spaces.Box(0, 500, self.simulation_time + 4)


        self.steps_beyond_done = None
        return np.array(self.state)


    def _render(self, mode='human', close=False):
        #TODO: Clean up plotting routine

        return None
        # if mode == 'rgb_array':
            # return None
        # elif mode is 'human':
            # if not bool(plt.get_fignums()):
                # plt.ion()
                # self.fig = plt.figure()
                # self.ax = self.fig.add_subplot(111)
                # # self.line1, = ax.plot(self.bg_history)
                # self.ax.plot(self.bg_history)
                # plt.show()
            # else:
                # # self.line1.set_ydata(self.bg_history)
                # # self.fig.canvas.draw()
                # self.ax.clear()
                # self.ax.plot(self.bg_history)

            # plt.pause(0.0000001)
            # plt.show()

            # # return None
        # else:
            # super(HovorkaInterval, self).render(mode=mode) # just raise an exception

            # plt.ion()
            # plt.plot(self.bg_history)

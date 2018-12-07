import numpy as np

def calculate_reward(blood_glucose_level, reward_flag='absolute', bg_ref=108, action=None, blood_glucose_level_start=None):
    """
    Calculating rewards for the given blood glucose level
    """

    if reward_flag == 'binary':
        ''' Binary reward function'''
        low_bg = 70
        high_bg = 120

        if np.max(blood_glucose_level) < high_bg and np.min(blood_glucose_level) > low_bg:
            reward = 1
        else:
            reward = 0

    elif reward_flag == 'binary_tight':
        ''' Tighter version of the binary reward function,
        the bounds are [-5, 5] around the optimal rate.
        '''
        # low_bg = bg_ref - 5
        # high_bg = bg_ref + 5
        low_bg = bg_ref - 10
        high_bg = bg_ref + 10

        if np.max(blood_glucose_level) < high_bg and np.min(blood_glucose_level) > low_bg:
            reward = 1
        else:
            reward = 0


    elif reward_flag == 'squared':
        ''' Squared cost function '''

        reward = - (blood_glucose_level - bg_ref)**2

    elif reward_flag == 'absolute':
        ''' Absolute cost function '''

        reward = - abs(blood_glucose_level - bg_ref)

    elif reward_flag == 'absolute_with_insulin':
        ''' Absolute cost with insulin constraint '''

        if action == None:
            action = [0, 0]

        # Parameters
        alpha = .7
        beta = 1 - alpha

        reward = - alpha*(abs(blood_glucose_level - bg_ref)) - beta * (abs(action[1]-action[0]))

    elif reward_flag == 'gaussian':
        ''' Gaussian reward function '''
        # h = 30
        h = 15

        reward = np.exp(-0.5 * (blood_glucose_level - bg_ref)**2 /h**2)

    elif reward_flag == 'gaussian_with_insulin':
        ''' Gaussian reward function '''
        # h = 30
        h = 15
        alpha = .5

        bg_reward = np.exp(-0.5 * (blood_glucose_level - bg_ref)**2 /h**2)
        insulin_reward =  -1/15 * action + 1

        reward = alpha * bg_reward + (1 - alpha) * insulin_reward

    elif reward_flag == 'hovorka':
        ''' Sum of squared distances from target trajectory in Hovorka 2014 '''
        trgt = 6 #bg_ref/18? target bg is 6 mmol/l in Hovorka 2014

        # starting state added as input to calculate_reward
        y0 = blood_glucose_level_start/18

        # time until blood glucose has decreased to trgt+2 if y0 > trgt+2
        t1 = np.max((y0-trgt-2)/2,0)

        # exponential half-time is 15 minutes (1/4h)
        r = 4*np.log(2)

        # target trajectory where starting bg is y0, time is in hours
        y = lambda t: trgt + (y0-trgt-2*t)*(y0-2*t>trgt+2) + (y0-trgt-t1-t)*(trgt<y0-t1-t<=trgt+2) - (trgt-y0)*np.exp(-r*t)*(y0<trgt)

        #how the index in blood_glucose_level relates to time in hours
        t = lambda i: i/60

        reward = 0
        for i in range(len(blood_glucose_level)):
            reward = reward - (blood_glucose_level[i]/18 - y(t(i)))**2


    return reward

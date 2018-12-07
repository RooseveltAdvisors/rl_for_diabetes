import numpy as np
import gym
# import seaborn as sns
# sns.set()

from pylab import plot, figure, title, show, ion, legend

env = gym.make('HovorkaGaussian-v0')
# env = gym.make('HovorkaGaussianInsulin-v0')
# env = gym.make('HovorkaBinary-v0')
# env = gym.make('HovorkaAbsolute-v0')


# basal = 0
# env.env.reset_basal_manually = 6.43

reward = []
bg = []
cgm = []

# env.env.reset_basal_manually = 6.43
env.env.bolus = 8.3
env.reset()

for i in range(48):

    # Step for the minimal/hovorka model
    s, r, d, i = env.step(np.array([-1]))
    # s, r, d, i = env.step(np.array([0]))
    bg.append(env.env.simulation_state[4])
    cgm.append(env.env.simulation_state[-1] * env.env.P[12])
    reward.append(r)
    # print(r)

    # Step for the discrete Hovorka incremental
    # env.step(2)



# env.render()
# figure()
# # plot(env.env.bg_history)
# plot(bg)
# plot(cgm)
# legend(['bg', 'cgm'])
# title('bg and cgm')
# ion()
# show()
plot(env.env.bg_history)
show()

from gym.envs.registration import registry, register, make, spec
from datetime import datetime
# ================================================
# Hovorka interval with different rewards and meals
# ================================================
register(
        id = 'HovorkaGaussian-v0',
        entry_point = 'gym_envs.hovorka_model.hovorka_interval_meals_gaussian:HovorkaGaussian',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'HovorkaBinary-v0',
        entry_point = 'gym_envs.hovorka_model.hovorka_interval_meals_binary:HovorkaBinary',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'HovorkaBinaryTight-v0',
        entry_point = 'gym_envs.hovorka_model.hovorka_interval_meals_binary_tight:HovorkaBinaryTight',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'HovorkaGaussianInsulin-v0',
        entry_point = 'gym_envs.hovorka_model.hovorka_interval_meals_gaussian_with_insulin:HovorkaGaussianInsulin',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'HovorkaAbsolute-v0',
        entry_point = 'gym_envs.hovorka_model.hovorka_interval_meals_absolute:HovorkaAbsolute',
        timestep_limit = 48,
        max_episode_steps= 48
        )

# ================================================
# Cambridge model
# ================================================

# register(
#         id = 'Cambridge-v0',
#         entry_point = 'gym_envs.cambridge_hovorka_model:CambridgeBase',
#         timestep_limit = 96,
#         max_episode_steps= 96
#         )
register(
        id = 'CambridgeGaussian-v0',
        entry_point = 'gym_envs.cambridge_hovorka_model.cambridge_gaussian:CambridgeGaussian',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'CambridgeBinary-v0',
        entry_point = 'gym_envs.cambridge_hovorka_model.cambridge_binary:CambridgeBinary',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'CambridgeBinaryTight-v0',
        entry_point = 'gym_envs.cambridge_hovorka_model.cambridge_binary_tight:CambridgeBinaryTight',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'CambridgeGaussianInsulin-v0',
        entry_point = 'gym_envs.cambridge_hovorka_model.cambridge_gaussian_insulin:CambridgeGaussianInsulin',
        timestep_limit = 48,
        max_episode_steps= 48
        )
register(
        id = 'CambridgeAbsolute-v0',
        entry_point = 'gym_envs.cambridge_hovorka_model.cambridge_absolute:CambridgeAbsolute',
        timestep_limit = 48,
        max_episode_steps= 48
        )

# ================================================
# Simglucose
# ================================================

# custom reward function
def custom_reward(BG_last_hour):
    if BG_last_hour[-1] > 180:
        return -1
    elif BG_last_hour[-1] < 70:
        return -2
    else:
        return 1
    
# specify start_time as the beginning of today
now = datetime.now()
start_time = datetime.combine(now.date(), datetime.min.time())

# custom scenario is a list of tuples (time, meal_size)
scen = [(7, 45), (12, 70), (16, 15), (18, 80), (23, 10)]


register(
    id='simglucose-adolescent2-v0',
    entry_point='gym_envs.simglucose_env.simglucose_gym_env:T1DSimEnv',
    kwargs={'patient_name': 'adolescent#001', 
            'pump_name': 'Insulet',
            'sensor_name': 'Dexcom', 'reward_fun': custom_reward, 
            'scen':scen, 'start_time':start_time}
)

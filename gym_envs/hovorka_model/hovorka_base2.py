import hovorka_base

class HovorkaBase2(hovorka_base.HovorkaBase):

    def _update_parameters(self):
        ''' Update parameters of model,
        this is only used for inherited classes'''

        meal_times = [240, 1000]
        meal_amounts = [100, 100]
        reward_flag = 'absolute'

        # Initialization flag: 'random' or 'fixed'
        bg_init_flag = 'random'

        return meal_times, meal_amounts, reward_flag, bg_init_flag

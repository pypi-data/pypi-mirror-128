from gym.envs.registration import register

register(
    id='qyc_enc-v0',
    entry_points='qyc_env.envs:QycEnv',
)
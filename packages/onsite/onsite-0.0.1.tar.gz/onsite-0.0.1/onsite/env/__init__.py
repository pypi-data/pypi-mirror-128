from .env_openx import EnvOpenx

def make(path):
    env = EnvOpenx()
    observation = env.init(path)
    return env,observation
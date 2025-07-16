from environs import Env

env = Env(expand_vars=True)

env.read_env()


class Enviroment:

    def __init__(self):
        self.BOT_TOKEN = env.str("BOT_TOKEN")
        self.POSTGRES_USER = env.str("POSTGRES_USER")
        self.POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
        self.POSTGRES_PORT = env.int("POSTGRES_PORT")
        self.POSTGRES_DB = env.str("POSTGRES_DB")
        self.OLLAMA_URL = env.str("OLLAMA_URL")
        self.OLLAMA_MODEL = env.str("OLLAMA_MODEL")


enviroment = Enviroment()

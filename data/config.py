from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
PAYMENTS_TOKEN = env.str("PAYMENTS_TOKEN")
DB_URI = env.str("DB_URI")
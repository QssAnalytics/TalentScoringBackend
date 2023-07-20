from talent_score.settings.base import *
import os, environ

env = environ.Env()
environ.Env.read_env()

if os.getenv("ENV_NAME")  == "LOCAL":
    from talent_score.settings.local import *

else :
    from talent_score.settings.product import *
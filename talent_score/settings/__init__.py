from .base import *
import os, environ

env = environ.Env()
environ.Env.read_env()

if env("ENV_NAME") == "LOCAL":
    from .local import *

else :
    from .product import *
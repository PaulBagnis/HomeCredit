from decouple import config
import os

class Devconfig:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_dict = {
    'development': Devconfig
}

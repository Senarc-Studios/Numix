import os
import utils

os.system(utils.get_command("pip") + " install -r requirements.txt")
os.system(utils.get_command("python") + " main.py")
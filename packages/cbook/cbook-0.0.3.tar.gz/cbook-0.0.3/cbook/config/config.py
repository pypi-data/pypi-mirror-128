import configparser
import os
 

app_name = "cbook"
config_folder = os.path.join(os.path.expanduser("~"), '.config', app_name)
os.makedirs(config_folder, exist_ok=True)

settings_file = "settings.conf"

full_config_file_path = os.path.join(config_folder, settings_file)
 
config = configparser.ConfigParser()

# init config
config['DEFAULT'] = {"recipe_path" : ""}

if not os.path.exists(full_config_file_path) or os.stat(full_config_file_path).st_size == 0:
    with open(full_config_file_path, 'w') as configfile:
        config.write(configfile)


def get_recipe_path():
    config.read(full_config_file_path)
    return config['DEFAULT']['recipe_path']


def set_recipe_path(path):
    config['DEFAULT']['recipe_path'] = path
    with open(full_config_file_path, 'w') as configfile:
        config.write(configfile)

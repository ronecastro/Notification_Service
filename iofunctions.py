import configparser, socket, pickle
from os import path

def current_path(file=None):
    try:
        dir_path = path.dirname(path.realpath(__file__), )
        if file != None:
            config_path = path.join(dir_path, file)
            return config_path
        else:
            return dir_path
    except Exception as e:
        return e

def fromcfg(section,key):
    try:
        fullpath = current_path('config.cfg')
        config = configparser.RawConfigParser()
        config.read_file(open(fullpath))
        r = config.get(section,key)
    except:
        return "error on reading 'config.cfg' file"
    return r

def write(filepath, msg):
    try:
        f = open(filepath, 'a')
        f.write(msg)
        f.close
        return 'ok'
    except Exception as e:
        return e

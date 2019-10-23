import pickle
import os.path


def SaveObject(obj, name):
    with open('objects/' + name + '.pkl', 'wb') as f:  # dump files into objects folder
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def LoadObject(name):
    with open('objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def FileExists(name):
    return os.path.exists('objects/' + name + '.pkl')

import pickle
import os.path

RootFolder = "C:/Users/steve/Documents/apps/mame-ai/Python/"

def SaveObject(obj, name):
    with open(RootFolder + 'objects/' + name + '.pkl', 'wb+') as f:  # dump files into objects folder
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def LoadObject(name):
    with open(RootFolder + 'objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def FileExists(name):
    return os.path.exists(RootFolder + 'objects/' + name + '.pkl')

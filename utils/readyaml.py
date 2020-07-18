import yaml

def readyml(filepath):

    f=open(filepath,encoding='UTF-8')
    ret=yaml.load(f,Loader=yaml.FullLoader)
    f.close()

    return ret
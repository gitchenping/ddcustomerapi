
import os
from utils.readini import readini

class LoadEnvData():
    _father_path = os.path.dirname(os.path.dirname(__file__))

    _presetvarinifilepath = _father_path + "\\config\\presetvar.ini"
    _testenvinifilepath = _father_path + "\\config\\testenv.ini"


    cf_presetvar = readini(_presetvarinifilepath)

    cf_testenv = readini(_testenvinifilepath)






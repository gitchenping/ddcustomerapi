import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.set_combine_reslut_returncode_enum import SetCombineResultReturnCodeEnum


class SetCombineResult():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\set_combine_result.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_combineapi_host', 'host') + LoadEnvData.cf_testenv.get('test_combineapi_host', 'set_combine_result_path')

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['custid'] = ""
        status_error_code = SetCombineResultReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    def setresult_ok(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['custid'] =LoadEnvData.cf_presetvar.get('combine','combine_cust_id')
        status_error_code = SetCombineResultReturnCodeEnum.SUCCESS.value
        return params_dict, status_error_code


def data_list():

    data_driven_list=[]
    setbineresult = SetCombineResult()

    data_driven_list+=[setbineresult.params_invalid(), \
                       setbineresult.setresult_ok()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.setcombineresult
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_SetCombineResult(pyfixture):

    #请求
    url=SetCombineResult.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]





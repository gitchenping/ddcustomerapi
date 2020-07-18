import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.get_combine_relation_returncode_enum import GetCombineRelationReturnCodeEnum


class GetCombineRelation():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\get_combine_relation.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_combineapi_host', 'host') + LoadEnvData.cf_testenv.get('test_combineapi_host', 'get_combine_relation_path')

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['custid'] = "123xxx"
        status_error_code = GetCombineRelationReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code


    def get_combine_relation_success(self):
        '''获取账户主子关系成功'''
        params_dict = dict(self.initparams)

        params_dict['custid']=LoadEnvData.cf_presetvar.get('combine','combine_cust_id')

        status_error_code = GetCombineRelationReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    combinerelation = GetCombineRelation()

    data_driven_list+=[combinerelation.params_invalid(), \
                       combinerelation.get_combine_relation_success()
                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.get_combine_relation
@pytest.mark.flaky(reruns=1,reruns_delay=60)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=GetCombineRelation.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]





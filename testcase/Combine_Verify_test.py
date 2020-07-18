import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.combine_verify_returncode_enum import CombineVerifyReturnCodeEnum

class CombineVerify():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\combine_verify.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_combineapi_host', 'host') + LoadEnvData.cf_testenv.get('test_combineapi_host', 'combine_verify_path')

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为空

        params_dict['custid'] = ""
        status_error_code = CombineVerifyReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code


    def cancel_deny(self):
        '''用户已申请注销'''

        params_dict = dict(self.initparams)

        # custid替换为空

        params_dict['custid'] = LoadEnvData.cf_presetvar.get('combine', 'custid_cancel')

        status_error_code = CombineVerifyReturnCodeEnum.CUSTID_ALREADY_APPLY_CANCEL.value

        return params_dict, status_error_code


    def custid_binded(self):
        '''子账号已合并过'''

        params_dict = dict(self.initparams)

        # custid替换为空

        params_dict['custid'] = LoadEnvData.cf_presetvar.get('combine','cust_id')

        status_error_code = CombineVerifyReturnCodeEnum.CUSTID_COMBINE_REPEAT_VERIFY_FAIL.value

        return params_dict, status_error_code

    def custid_enterprise_deny(self):
        '''企业账号不具备合并条件'''

        params_dict = dict(self.initparams)

        # custid替换为企业账号

        params_dict['custid'] = LoadEnvData.cf_presetvar.get('combine', 'enterprise_cust_id')

        status_error_code = CombineVerifyReturnCodeEnum.CUSTID_DENY_FOR_ENTERPRISE_FAIL.value

        return params_dict, status_error_code


    def custid_veify_ok(self):
        '''可以合并'''
        params_dict = dict(self.initparams)

        #不在customer_combine表中的custid
        params_dict['custid'] = LoadEnvData.cf_presetvar.get('combine', 'cust_bind_weixin')

        status_error_code = CombineVerifyReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code





def data_list():

    data_driven_list=[]
    combineverify = CombineVerify()

    data_driven_list+=[combineverify.params_invalid(), \
                        combineverify.custid_binded(),\
                       #combineverify.cancel_deny(),\
                       combineverify.custid_enterprise_deny(),\
                       combineverify.custid_veify_ok()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.combineverify
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_CombineVerifyDelete(pyfixture):

    #请求
    url=CombineVerify.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]





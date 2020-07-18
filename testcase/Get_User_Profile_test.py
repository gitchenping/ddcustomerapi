import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.get_user_profile_returncode_enum import GetUserProfileReturnCodeEnum

class GetUserProfile():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\get_user_profile.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_profileapi_host', 'host') + LoadEnvData.cf_testenv.get('test_profileapi_host', 'get_user_profile_path')

    def __init__(self):

        pass

    def custid_invalid(self):
        '''custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['cust_id'] = "123xxx"
        status_error_code = GetUserProfileReturnCodeEnum.CUSTID_WRONG.value

        return params_dict, status_error_code

    def keyword_invalid(self):
        '''keyword不正确'''
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = LoadEnvData.cf_presetvar.get('profile','cust_id')
        # keyword替换为非法字符

        params_dict['keyword'] = "xxxxxx"
        status_error_code = GetUserProfileReturnCodeEnum.KEWWORDWRONG.value

        return params_dict, status_error_code

    def empty_search(self):
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = '12345678'     #custid不存在
        params_dict['keyword']=''
        status_error_code = GetUserProfileReturnCodeEnum.EMPTYINFO.value

        return params_dict, status_error_code


    def getuserprofile_success(self):
        '''获取用户档案信息成功'''

        params_dict = dict(self.initparams)

        params_dict['cust_id'] = LoadEnvData.cf_presetvar.get('profile', 'cust_id')

        status_error_code = GetUserProfileReturnCodeEnum.SUCCESS.value

        params_dict_list = []
        # keyword展开
        for ele in params_dict['keyword']:

            params_dict['keyword']=ele

            params_dict_list.append((params_dict,status_error_code))

        return params_dict_list


def data_list():

    data_driven_list=[]
    getuserprofile = GetUserProfile()

    data_driven_list+=[getuserprofile.custid_invalid(), \
                       getuserprofile.keyword_invalid(),\
                       getuserprofile.empty_search()
                       ]+getuserprofile.getuserprofile_success()

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.getuserprofile
@pytest.mark.flaky(reruns=1,reruns_delay=60)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=GetUserProfile.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['errorCode']==pyfixture[1][0]





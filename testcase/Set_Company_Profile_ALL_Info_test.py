import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.set_company_profile_all_info_returncode_enum import SetCompanyProfileAllInfoReturnCodeEnum

class SetCompanyProfileAllInfo():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\set_company_profile_all_info.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_profileapi_host', 'host') + LoadEnvData.cf_testenv.get('test_profileapi_host',\
                                                                                                  'set_company_profile_all_info_path')

    def __init__(self):

        pass

    def custid_invalid(self):
        '''custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为空
        params_dict['cust_id'] = ""
        status_error_code = SetCompanyProfileAllInfoReturnCodeEnum.CUSTID_WRONG.value

        return params_dict, status_error_code


    def company_long(self):
        '''cust_company的长度大于100'''
        params_dict = dict(self.initparams)

        params_dict['cust_id']=LoadEnvData.cf_presetvar.get('profile','enterprise_cust_id')
        params_dict['cust_company']=''.join('a' for i in range(102))

        status_error_code = SetCompanyProfileAllInfoReturnCodeEnum.COMPANY_LONG.value

        return params_dict, status_error_code


    def province_city_town_null(self):
        '''cust_province_id/cust_city_id/cust_town_id/cust_quarter_id 是空'''

        params_dict = dict(self.initparams)

        params_dict['cust_id'] = LoadEnvData.cf_presetvar.get('profile', 'enterprise_cust_id')

        params_dict['cust_province_id']=''
        params_dict['cust_city_id'] = ''

        status_error_code = SetCompanyProfileAllInfoReturnCodeEnum.PROVINCE_TOWN_QUARTER_EMPTY.value

        return params_dict, status_error_code


    def setcompanyallinfo_success(self):
        '''修改完毕'''
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = LoadEnvData.cf_presetvar.get('profile', 'enterprise_cust_id')

        status_error_code = SetCompanyProfileAllInfoReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    setcompanyprofileallinfo = SetCompanyProfileAllInfo()

    data_driven_list+=[setcompanyprofileallinfo.custid_invalid(), \
                       setcompanyprofileallinfo.company_long(),\
                       setcompanyprofileallinfo.province_city_town_null(), \
                       setcompanyprofileallinfo.setcompanyallinfo_success()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.setcompanyprofileallinfo
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=SetCompanyProfileAllInfo.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['errorCode']==pyfixture[1][0]

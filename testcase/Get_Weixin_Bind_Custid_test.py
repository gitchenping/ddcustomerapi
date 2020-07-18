import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.get_weixin_bind_custid_returncode_enum import GetWeixinBindCustidReturnCodeEnum

class GetWeixinBindCustid():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\get_weixin_bind_custid.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_combineapi_host', 'host') + LoadEnvData.cf_testenv.get('test_combineapi_host', 'get_weixin_bind_custid_path')

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # unionid替换为非法字符

        params_dict['unionid'] = ""
        status_error_code = GetWeixinBindCustidReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code


    def weixin_notbind_custid(self):
        '''未绑定'''
        params_dict = dict(self.initparams)

        #从库里获取一个未绑定的账户
        sql='select wx_union_id from customer_third_wechat where cust_bind_type=2 limit 1; '

        unionid=MysqlGet(sql)
        params_dict['unionid'] = unionid

        status_error_code = GetWeixinBindCustidReturnCodeEnum.NOT_COMBINED.value

        return params_dict, status_error_code


    def weixin_bind_custid(self):
        '''已绑定'''
        params_dict = dict(self.initparams)

        params_dict['unionid'] = LoadEnvData.cf_presetvar.get('combine','cust_bind_weixin_unionid')

        status_error_code = GetWeixinBindCustidReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

        pass




def data_list():

    data_driven_list=[]
    getweixinbindcustid = GetWeixinBindCustid()

    data_driven_list+=[getweixinbindcustid.params_invalid(), \
                        getweixinbindcustid.weixin_notbind_custid(),\
                       getweixinbindcustid.weixin_bind_custid()
                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.getweixinbindcustid
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_GetWeixinBindCustid(pyfixture):

    #请求
    url=GetWeixinBindCustid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]





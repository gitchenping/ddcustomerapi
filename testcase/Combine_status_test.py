import os
import pytest
import time
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import MysqlGet,MysqlInsert
from data.globaldataload import LoadEnvData
from data.combine_status_returncode_enum import CombineStatusReturnCodeEnum

class CombineStatus():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\combine_status.yml"
    initparams = readyml(yamlfilepath)

    url = LoadEnvData.cf_testenv.get('test_combineapi_host', 'host') + LoadEnvData.cf_testenv.get('test_combineapi_host', 'combine_status_path')

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['custid'] = "123xxx"
        status_error_code = CombineStatusReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code


    def combine_notweixin(self):
        '''非微信账号，即主站账号'''

        params_dict = dict(self.initparams)

        #从库里获取一个主站账户
        sql='select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat union ' \
            ' select cust_id from customer_third) and cust_id>0 limit 1'

        custid=MysqlGet(sql)
        params_dict['custid'] = custid

        status_error_code = CombineStatusReturnCodeEnum.NOT_WEIXIN.value

        return params_dict, status_error_code


    def combine_done(self):
        '''合并完成'''

        params_dict = dict(self.initparams)

        #在customer_third_wechat表中找到一条cust_bind_type=1的custid 或找一个绑定过微信的custid

        params_dict['custid'] =LoadEnvData.cf_presetvar.get('combine','cust_bind_weixin')

        status_error_code = CombineStatusReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

    def combine_notdo(self):
        '''未合并'''

        params_dict = dict(self.initparams)

        #从customer_third_wechat表中找到一条cust_bind_type=2的custid，该custid作为子账号在customer_combine表不存在

        sql='select cust_id from customer_third_wechat where cust_bind_type=2 and cust_id not in (select cust_id from customer_combine ' \
            ') limit 1'

        custid = MysqlGet(sql)
        params_dict['custid'] = custid

        status_error_code = CombineStatusReturnCodeEnum.NOT_COMBINED.value

        return params_dict, status_error_code

    def combine_doing(self):
        '''合并进行中'''

        params_dict = dict(self.initparams)

        #用主账号在customer_combine_process中查询数据

        params_dict['custid'] = LoadEnvData.cf_presetvar.get('combine','combine_cust_id')

        status_error_code = CombineStatusReturnCodeEnum.COMBINE_DOING.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    combinestatus = CombineStatus()

    data_driven_list+=[combinestatus.params_invalid(), \
                       combinestatus.combine_notweixin(),\
                       combinestatus.combine_done(),\
                       combinestatus.combine_notdo(),\
                       combinestatus.combine_doing()
                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.combinestatus
@pytest.mark.flaky(reruns=1,reruns_delay=60)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=CombineStatus.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]





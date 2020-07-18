import os
import pytest
import allure
from utils.requesttool import request
from utils.readyaml import readyml
from utils.readini import readini
from utils.pysql import PyMySQL1
from data.weixin_bind_custid_returncode_enum import WeixinBindCustidReturnCodeEnum


class Weixin_Bind_Custid():

    father_path=os.path.dirname(os.path.dirname(__file__))

    yamlfilepath = father_path + "\\data\\weixin_bind_custid.yml"
    presetvarinifilepath = father_path + "\\config\\presetvar.ini"
    testenvinifilepath=father_path+"\\config\\testenv.ini"

    initparams = readyml(yamlfilepath)
    cf_presetvar = readini(presetvarinifilepath)
    cf_testenv=readini(testenvinifilepath)

    url = cf_testenv.get('test_loginapi', 'host') + cf_testenv.get('test_loginapi', 'weixin_bind_custid_path')

    def __init__(self):
        pass

    def custid_notindb(self):
        '''custid不存在'''

        params_dict = dict(self.initparams)

        status_error_code =WeixinBindCustidReturnCodeEnum.CUSTID_NOT_FIND.value

        return params_dict, status_error_code


    def custid_binded(self):
        '''当前custid已绑定过其它微信'''
        params_dict = dict(self.initparams)

        #custid替换为库里已绑定过微信的custid
        params_dict['custid'] = self.cf_presetvar.get('login', 'cust_bind_weixin')

        status_error_code = WeixinBindCustidReturnCodeEnum.CUSTID_BINDED.value

        return params_dict, status_error_code

    def weixin_binded(self):
        '''当前微信曾绑定过其它custid'''
        params_dict = dict(self.initparams)

        #1.从库里选择一个未绑定过微信的custid
        sql='select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat) and cust_id>0 limit 1;'
        custid=PyMySQL1().mysqlget(sql)

        #2.从库里选择一个微信union_id(该union_id必被绑定过）
        sql='select wx_union_id from customer_third_wechat where cust_bind_type=2 limit 1; '
        unionid = PyMySQL1().mysqlget(sql)

        #3.更新组合参数
        params_dict['custid']=custid
        params_dict['union_id']=unionid

        status_error_code = WeixinBindCustidReturnCodeEnum.WEIXIN_BINDED.value

        return params_dict, status_error_code

    def weixin_binc_custid_success(self):
        '''绑定成功'''
        params_dict = dict(self.initparams)
        # 1.从库里选择一个未绑定过微信的custid
        sql = 'select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat) limit 1;'
        custid = PyMySQL1().mysqlget(sql)

        # 2.更新组合参数
        params_dict['custid'] = custid

        status_error_code = WeixinBindCustidReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

def teardown_module():
    '''用例结果数据销毁'''

    #删除customer_third_wechat表
    PyMySQL1().mysqldel('customer_third_wechat', 'wx_union_id', Weixin_Bind_Custid.initparams['union_id'])

    #to do,其他表



def data_list():

    data_driven_list=[]
    weixinbindcustid = Weixin_Bind_Custid()

    data_driven_list+=[weixinbindcustid.custid_notindb(), \
                       weixinbindcustid.custid_binded(),\
                       weixinbindcustid.weixin_binded(),\
                       weixinbindcustid.weixin_binc_custid_success()
                       ]

    return data_driven_list



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_bind_custid
@pytest.mark.flaky(reruns=1,reruns_delay=60)
def test_WeixinBindCustid(pyfixture):

    #请求
    url=Weixin_Bind_Custid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['statusCode']==pyfixture[1][0]

    if res['statusCode']==WeixinBindCustidReturnCodeEnum.SUCCESS.value[0]:
        assert PyMySQL1().checkdbok('customer_third_wechat','wx_union_id',Weixin_Bind_Custid.initparams['union_id']),'''未写入数据库'''
        #assert PyMySQL().checkdbok('customer_third_wechat', 'wx_union_id',"232412134"), '''未写入数据库'''
    #return res0.

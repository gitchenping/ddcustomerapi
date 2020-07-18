import pytest

if __name__=="__main__":
    pytest.main(["--alluredir=report",\
                 "-m" ,\
                 #"weixin_register or "
                 #" weixin_bind_custid"
                 #"weixin_unbind_delete"
                #"get_combine_relation"
                 #"combinestatus"
                 #"getuserprofile"
                 #"setuserprofile"
                 #"changeprofileimg"
                 #"setcompanyprofileallinfo"
                 #"setuserprofileallinfo"
                 #"weixinverify"
                 #"getweixinbindcustid"
                 #"combineverify"
                 #"getcombineresult"
                 "setcombineresult"
                 ])
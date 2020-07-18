import requests
import json

def request(requestmethod='get', url=None, data=None, cookies=None):
    """

    :param requestmethod:
    :param url:
    :param data: 字典类型，如{"key1":value1,"key2":value2}
    :return:
    """
    if requestmethod in ['post', 'POST', 'Post']:
        res = requests.post(url, data=data, cookies=cookies)
    else:
        res = requests.get(url, params=data, cookies=cookies)

    if res.status_code !=200:
        return "请求失败！"

    res_dict=json.loads(res.text)

    return res_dict


def requestsession(requestmethod='get', url=None, data=None):
    """

    :param requestmethod:
    :param url:
    :param data:
    :return:
    """
    s = requests.session()
    if requestmethod in ['post', 'POST', 'Post']:
        res = s.post(url, data=data)
    else:
        print("wrong request method!")
        return

    res = s.get(url, params=data)

    return res

import json
import warnings

import requests
import re
from urllib import parse
import time
import threading

from wxpusher import WxPusher

from tools import utils
from tools.jd_sign import getSign


warnings.filterwarnings("ignore")


def getUrlParams(url):
    res = dict(parse.parse_qsl(url))
    return res


def get_cookie_string(cookie):
    cookie_string = ""
    for cookie_key in cookie.keys():
        cookie_string += "%s=%s;" % (cookie_key, cookie[cookie_key])
    return cookie_string


def get_jd_time():
    response = requests.get(
        url="https://api.m.jd.com/client.action?functionId=queryMaterialProducts&client=wh5"
    )
    print(response.json())


def get_sk(data):
    data_val = [val for val in data["data"].values()]
    n, o, p, q, r, s = (
        data_val[0],
        data_val[1],
        data_val[2],
        data_val[3],
        data_val[4],
        data_val[5],
    )
    sk_val = ""
    if n == "cca":
        sk_val = p[14:19].lower() + o[5:15].upper()
    if n == "ab":  # check ok
        sk_val = r[10:18] + s[2:13].lower()
    if n == "ch":
        sk_val = q.upper() + r[6:10].upper()
    if n == "cbc":  # check ok
        sk_val = q[3:13].upper() + p[10:19].lower()
    if n == "by":
        sk_val = o[5:8] + re.sub("a", "c", p, flags=re.IGNORECASE)
    if n == "xa":
        sk_val = o[1:16] + s[4:10]
    if n == "cza":
        sk_val = q[6:19].lower() + s[5:11]
    if n == "cb":
        sk_val = s[5:14] + p[2:13].upper()

    return sk_val


class JDSecKillAPI:
    def __init__(self, sku, ck):
        self.skuId = sku
        self.s = requests.session()
        self.sku = sku
        self.ck = ck
        self.aid = ""
        self.eid = "eidIc11281210cs70PmWgaoKQzC+zNCtvs4P3dD5mAuShiRsxafFMGVcd10/Y4VCZCU/TnJEc6QPJEiD47thQMk59x2tMJP7F4iy1qs4jVhEKMSQBNx6"
        self.uuid = "f3a6322845f49a67b1e531c8338141bc4073e3cd"
        self.uts = "0f31TVRjBSsqndu4/jgUPz6uymy50MQJa7SeBOkP/uv4N6snXVJWRt4VGrM0HA5I4ui492xEpEufAD25f3pYNBemlwQX2SpBmrz7LA/Z1OaXg8NpotnDR31DZM00iFHc2xESEZe1g7R3oA/28uOn6vtPsxuck4f3lTfmoeowGvp4mFcdtDywWcqZ/qlhzGY5RtH2ePex0kOJOQtvHHavKQ=="
        self.wifiBssid = "e965f6de0e3d368c765ea7b31f699302"
        self.ua = "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36"
        # self.ua = 'Mozilla/5.0 (Linux; Android 12; 22021211RC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046011 Mobile Safari/537.36'
        self.ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1"



    def appoint_sku(self):
        headers = {
            "user-agent": "JD4iPhone/168898%20(iPhone;%20iOS;%20Scale/2.00);jdmall;iphone;version/12.1.4;build/168898;network/wifi;screen/828x1792;os/16.6",
            "X-Rp-Client": "ios_3.0.0",
            # 'content-type': 'application/x-www-form-urlencoded',
            "cookie": self.ck,
            "jdc-backup": self.ck,
        }

        ts = int(time.time() * 1000)
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)
        query_params = {
            "functionId": "appoint",
            "clientVersion": "12.1.4",
            "build": "168898",
            "client": "apple",
            "d_brand": "apple",
            "d_model": "iPhone11,8",
            "osVersion": "16.6",
            "screen": "828*1792",
            "partner": "apple",
            "aid": self.aid,
            "eid": self.eid,
            "sdkVersion": "29",
            "lang": "zh_CN",
            # 'harmonyOs': '0',
            "uuid": self.uuid,
            "area": "12_919_922_23977",
            "networkType": "wifi",
            "wifiBssid": self.wifiBssid,
            "uts": self.uts,
            "uemps": "0-0-0",
            "ext": '{"prstate":"0","pvcStu":"1"}',
            # 'ef': '1',
            # 'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }
        reserve_url = "https://api.m.jd.com/client.action"

        body = {
            "autoAddCart": "0",
            "bsid": "",
            "check": "0",
            "ctext": "",
            "isShowCode": "0",
            "mad": "0",
            "skuId": self.skuId,
            "type": "1",
        }

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params["functionId"],
            "uuid": uuid,
            "client": query_params["client"],
            "clientVersion": query_params["clientVersion"],
            "body": json.dumps(body, ensure_ascii=False, separators=(",", ":")),
        }
        st, sign, sv = getSign(plainTextDic)

        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)

        data = {"body": json.dumps(body, ensure_ascii=False, separators=(",", ":"))}

        response = self.s.post(
            url=reserve_url,
            params=query_params,
            data=data,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=3,
        )
        return response.json()

    def get_token_key(self):
        headers = {
            "user-agent": "JD4iPhone/168898%20(iPhone;%20iOS;%20Scale/2.00);jdmall;iphone;version/12.1.4;build/168898;network/wifi;screen/828x1792;os/16.6",
            "X-Rp-Client": "ios_3.0.0",
            # 'content-type': 'application/x-www-form-urlencoded',
            "cookie": self.ck,
            "jdc-backup": self.ck,
        }

        ts = int(time.time() * 1000)
        uuid = self.uuid
        ep = utils.get_ep(ts, uuid)

        query_params = {
            "functionId": "genToken",
            "clientVersion": "12.1.4",
            "build": "168898",
            "client": "apple",
            "d_brand": "apple",
            "d_model": "iPhone11,8",
            "osVersion": "16.6",
            "screen": "828*1792",
            "partner": "apple",
            "aid": self.aid,
            "eid": self.eid,
            "sdkVersion": "29",
            "lang": "zh_CN",
            # 'harmonyOs': '0',
            "uuid": self.uuid,
            "area": "12_919_922_23977",
            "networkType": "wifi",
            "wifiBssid": self.wifiBssid,
            "uts": self.uts,
            "uemps": "0-0-0",
            "ext": '{"prstate":"0","pvcStu":"1"}',
            # 'ef': '1',
            # 'ep': json.dumps(ep, ensure_ascii=False, separators=(',', ':')),
        }

        body = {
            "action": "to",
            "to": "https://divide.jd.com/user_routing?skuId=" + self.sku,
        }

        plainTextDic = {
            "st": ts,  # 毫秒级时间戳
            "sv": "120",
            "functionId": query_params["functionId"],
            "uuid": uuid,
            "client": query_params["client"],
            "clientVersion": query_params["clientVersion"],
            "body": json.dumps(body, ensure_ascii=False, separators=(",", ":")),
        }
        st, sign, sv = getSign(plainTextDic)

        query_params.update(st=st)
        query_params.update(sign=sign)
        query_params.update(sv=sv)

        data = {"body": json.dumps(body, ensure_ascii=False, separators=(",", ":"))}

        response = self.s.post(
            url="https://api.m.jd.com/client.action",
            params=query_params,
            data=data,
            headers=headers,
            allow_redirects=False,
            verify=False,
            timeout=3,
        )
        token_key = response.json()['tokenKey']
        print('Token Key: ----------> %s' % response.json())
        print(response.status_code)
        json_obj = response.json()
        print("Get genToken--------------->%s" % str(json_obj))
        return json_obj

    def get_appjmp(self, token_params):
        headers = {"user-agent": self.ua}
        appjmp_url = token_params["url"]
        params = {
            "to": "https://divide.jd.com/user_routing?skuId=%s" % self.skuId,
            "tokenKey": token_params["tokenKey"],
        }

        response = self.s.get(
            url=appjmp_url,
            params=params,
            allow_redirects=False,
            verify=False,
            headers=headers,
        )
        print("Get Appjmp跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def get_divide(self, divide_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=divide_url, allow_redirects=False, verify=False, headers=headers
        )
        print("Get Divide跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def get_captcha(self, captcha_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=captcha_url, allow_redirects=False, verify=False, headers=headers
        )
        print("Get Captcha跳转链接-------------->%s" % response.headers["Location"])
        return response.headers["Location"]

    def visit_seckill(self, seckill_url):
        headers = {"user-agent": self.ua}
        response = self.s.get(
            url=seckill_url, allow_redirects=False, verify=False, headers=headers
        )
        return response

    def init_action(self, num=1):
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            init_action_url = (
                "https://marathon.jd.com/seckillnew/orderService/init.action"
            )
            data = {
                "sku": self.skuId,
                "num": num,
                "id": 0,
                "provinceId": 0,
                "cityId": 0,
                "countyId": 0,
                "townId": 0,
            }
            response = self.s.post(
                url=init_action_url,
                data=data,
                allow_redirects=False,
                verify=False,
                headers=headers,
            )
            print("init action返回数据：%s" % response.text)
            # JDSecKillSubmit.log("init action返回数据：%s" % response.text)
            return response.json()
        except Exception as e:
            print(str(e))
            return None

    def get_tak(self):
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            tak_url = "https://tak.jd.com/t/871A9?_t=%d" % (
                int(round(time.time() * 1000))
            )
            response = self.s.get(
                url=tak_url, allow_redirects=False, verify=False, headers=headers
            )
            sk_val = get_sk(data=response.json())
            return sk_val
        except Exception as e:
            print(str(e))
            return ""

    def submit_order(self, order_data, sk):
        try:
            headers = {"user-agent": self.ua, "Connection": "keep-alive"}
            submit_order_url = (
                "https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=%s"
                % self.skuId
            )
            address_info = order_data["address"]
            invoice_info = order_data["invoiceInfo"]
            data = {
                "num": order_data["seckillSkuVO"]["num"],
                "addressId": address_info["id"],
                "yuShou": True,
                "isModifyAddress": False,
                "name": address_info["name"],
                "provinceId": address_info["provinceId"],
                "provinceName": address_info["provinceName"],
                "cityId": address_info["cityId"],
                "cityName": address_info["cityName"],
                "countyId": address_info["countyId"],
                "countyName": address_info["countyName"],
                "townId": address_info["townId"],
                "townName": address_info["townName"],
                "addressDetail": address_info["addressDetail"],
                "mobile": address_info["mobile"],
                "mobileKey": address_info["mobileKey"],
                "email": "",
                "invoiceTitle": invoice_info["invoiceTitle"],
                "invoiceContent": invoice_info["invoiceContentType"],
                "invoicePhone": invoice_info["invoicePhone"],
                "invoicePhoneKey": invoice_info["invoicePhoneKey"],
                "invoice": True,
                "codTimeType": "3",
                "paymentType": "4",
                "overseas": "0",
                "token": order_data["token"],
                "sk": sk,
            }
            
            response = self.s.post(
                url=submit_order_url,
                data=data,
                allow_redirects=False,
                verify=False,
                headers=headers,
                proxies=self.proxy
            )
            return response.json()
        except Exception as e:
            print("submit error--->" + str(e))
            return None

    def send_message(self, content):
        pass
        # try:
        #     # 推送token
        #     PUSH_TOKEN = "AT_4XxUFvSjSLWTlFhX1nFmIepe1RNoGq8b"

        #     UIDS = [
        #         "UID_D77yyDO0pT7K0f1q2UijDTGnGthF",
        #     ]
        #     msg = WxPusher.send_message(content, uids=UIDS, token=PUSH_TOKEN)
        # except Exception as e:
        #     print("send_message error--->" + str(e))



if __name__ == "__main__":
    ck = 'pin=jd_5b6fac6380384;wskey=AAJlI-2hAEBiqSXhg6VijFp-1lCSn2bfv33Q0U4doD6G77Lb0GHnovyxvKnJ5Z-gPJ2DQ_6Q0dZr4tt-q0POezIgXoVZzW5m;whwswswws=JD012145b9Q9csdRMl1j169685341424406_NUFlepjUQsqJNwxMjpv5GVsdiRu8msMFXcq85ba_y_gSfM59MoFS7TycyI1Mp1ceoRy5kLsadFXJEe2PEtXkyCDuK_n13rdH-2HE8HT3sg0k9ideg~AAudiVxSLEAAAAAAAAAAAAAAAAPXhUoWjgF6hQAAAAAA;unionwsws={"devicefinger":"eidA0079812291sbmBtg+WVyRJ6MQc\/d8Uydo5gbYoR5yar82DMDOblglNELd6MTGrwh1Uc4By5vvv+yqSQjPKRdLyu1PsPah0DHjg5WKleI6d9odY9G","jmafinger":"JD012145b9Q9csdRMl1j169685341424406_NUFlepjUQsqJNwxMjpv5GVsdiRu8msMFXcq85ba_y_gSfM59MoFS7TycyI1Mp1ceoRy5kLsadFXJEe2PEtXkyCDuK_n13rdH-2HE8HT3sg0k9ideg~AAudiVxSLEAAAAAAAAAAAAAAAAPXhUoWjgF6hQAAAAAA"};'
    jdapi = JDSecKillAPI("100012043978", ck)
    prom_date= jdapi.appoint_sku()
    print("返回信息--->", prom_date)
    json_data = json.loads(json.dumps(prom_date))
    title = json_data['title']
    print("gentoken结果--->", jdapi.get_token_key())
    print("预约结果--------------------------", title)


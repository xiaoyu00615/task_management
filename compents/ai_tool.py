# coding: utf-8
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
# 新增：用于线程同步的锁和事件
import threading


class AiTool(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)
    # 出错时也触发结束事件，避免主线程卡死
    ws.completion_event.set()


# 收到websocket关闭的处理
def on_close(ws):
    print("### closed ###")
    # 触发结束事件
    ws.completion_event.set()


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.response_content = f"请求错误: {code}, {data}"  # 错误信息存入缓存
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # 将内容追加到缓存中，而非直接打印
        ws.response_content += content
        # 可选：保留原打印功能，方便调试
        print(content, end='')
        if status == 2:
            print("\n#### 关闭会话")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请求参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": query}]
            }
        }
    }
    return data


def main(appid, api_secret, api_key, Spark_url, domain, query):
    # 初始化AI工具类
    wsParam = AiTool(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    # 创建WebSocket App实例
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)

    # 给ws对象添加自定义属性：用于缓存返回内容
    ws.response_content = ""
    # 给ws对象添加自定义属性：用于线程同步的事件（等待会话结束）
    ws.completion_event = threading.Event()

    # 绑定必要的参数到ws对象
    ws.appid = appid
    ws.query = query
    ws.domain = domain

    # 启动WebSocket（非阻塞）
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    # 等待会话结束（直到on_close/on_error触发）
    ws.completion_event.wait()

    # 返回最终拼接的完整内容
    return ws.response_content


if __name__ == "__main__":
    # 调用main函数并接收返回结果
    result = main(
        appid="9b86", # 有误不能直接使用
        api_secret="ODdkZDllM2YwNDQxOTVmYjV", # 有误不能直接使用
        api_key="468430ebb5584af07afe4e6", # 有误不能直接使用
        Spark_url="wss://spark-api.xf-yun.com/v1.1/chat",  # Lite环境的地址
        domain="lite",  # Lite版本
        query="你好" # 问题
    )

    # 打印返回的结果（现在你可以自由使用这个result变量）
    print("\n===== 最终返回结果 =====")
    print(result)
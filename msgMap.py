import logging
import time
from job_mgmt import Job
import random
import threading
from flask import Flask

class MsgMap(Job):
    def __init__(self) -> None:
        self.VerifyCode = None
        # self.VerifyCodes = {}
        self.CodeLock = threading.Lock()
        self.mp = {"验证码": self.GetVerifyCodeMsg, "帮助": "你可以回复：验证码"}
        self.onEveryMinutes(1, self.RenewVerifyCode)
        # 启动后端
        self.app = Flask(__name__)
        self.app.add_url_rule('/get_verify_code', 'get_verify_code', self.GetVerifyCode)
        threading.Thread(target=self.run_server).start()
        self.LOG = logging.getLogger("MsgMap")
        self.LOG.info("后端启动成功:http://127.0.0.1:8080/get_verify_code")

    def run_server(self):
        self.app.run(port=8080)

    def GetVerifyCodeMsg(self):
        return "请注意, 验证码每60秒刷新一次, 此次验证码为：\n" + str(self.GetVerifyCode())

    def GetVerifyCode(self):
        return self.VerifyCode or self.RenewVerifyCode()

    def RenewVerifyCode(self):
        code = ""
        for _ in range(5):
            code += str(random.randint(0, 9))
        with self.CodeLock:
            # self.VerifyCodes[code] = time.time()
            self.VerifyCode = code
        return code


# -*- coding:utf-8 -*-

"""
服务配置

Author: eternal ranger
Date:   2020/07/09
email: interstella.ranger2020@gmail.com
"""

import json

class Config:
    """服务配置"""

    def __init__(self):
        pass


    def loads(self, config_file=None):
        """
        加载配置。
        :param config_file:json配置文件
        :return:
        """
        with open(config_file) as json_file:
            configures = json.load(json_file)
        self.access_key = configures['EXCHANGE']['access_key']
        self.secret_key = configures['EXCHANGE']['secret_key']
        self.passphrase = configures['EXCHANGE']['passphrase']
        self.ding_talk_api = configures['DINGTALK']['ding_talk_api']
        self.accountSID = configures['TWILIO']['accountSID']
        self.authToken = configures['TWILIO']['authToken']
        self.myNumber = configures['TWILIO']['myNumber']
        self.twilio_Number = configures['TWILIO']['twilio_Number']
        self.from_addr = configures['SENDMAIL']['from_addr']
        self.password = configures['SENDMAIL']['password']
        self.to_addr = configures['SENDMAIL']['to_addr']
        self.smtp_server = configures['SENDMAIL']['smtp_server']
        self.level = configures['LOG']['level']
        self.handler = configures['LOG']['handler']

    def update_config(config_file = None):
        """"更新配置"""
        with open("config.json", 'w') as json_file:
            json.dump(config, json_file, indent=4)
        return None

config = Config()
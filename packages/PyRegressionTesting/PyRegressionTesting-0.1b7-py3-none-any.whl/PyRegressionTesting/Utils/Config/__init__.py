import json

from PyRegressionTesting.Utils.Config.TestsConfig import TestsConfig
from PyRegressionTesting.Utils.Config.MailConfig import MailConfig


class Config:
    def __init__(self, test_name, sender_mail_config, receiver_mail_config, tests_config):
        self.test_name = test_name
        self.sender_mail_config = sender_mail_config
        self.receiver_mail_config = receiver_mail_config
        self.tests_config = tests_config

    @staticmethod
    def from_json_file(path):
        file = open(path)
        json_data = json.load(file)
        return Config.from_json(json_data)

    @staticmethod
    def from_json(json_data):
        test_name = json_data['test_name']
        sender_mail_config = MailConfig.from_json(json_data['sender_mail'])
        receiver_mail_config = MailConfig.from_json(json_data['receiver_mail'])
        tests_config = TestsConfig.from_json(json_data['test_config'])
        return Config(test_name, sender_mail_config, receiver_mail_config, tests_config)
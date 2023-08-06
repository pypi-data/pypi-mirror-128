from PyRegressionTesting.TestModule.AssertModule import AssertModule
from PyRegressionTesting.TestModule.ClickModule import ClickModule
from PyRegressionTesting.TestModule.EmailModule import EmailModule
from PyRegressionTesting.TestModule.HoverModule import HoverModule
from PyRegressionTesting.TestModule.SetStorageModule import SetStorageModule
from PyRegressionTesting.TestModule.WaitModule import WaitModule
from PyRegressionTesting.TestModule.InputModule import InputModule


class TestsConfig:
    def __init__(self, name, url, pre_steps, test_steps):
        self.name = name
        self.url = url
        self.pre_steps = pre_steps
        self.test_steps = test_steps

    @staticmethod
    def from_json(json):
        pre_steps_config = json['pre_steps']
        
        pre_steps = []
        for step in pre_steps_config:
            pre_steps.append(TestsConfig.create_module_from_config(step))
        
        tests_config = []
        for test in json['tests']:
            test_steps = []
            for step in test['steps']:
                test_steps.append(TestsConfig.create_module_from_config(step))
            name = test['name']
            url = test['url']
            tests_config.append(TestsConfig(name, url, pre_steps, test_steps))

        return tests_config

    @staticmethod
    def create_module(type, config):
        if type == "wait":
            return WaitModule(type, config)
        elif type == "click":
            return ClickModule(type, config)
        elif type == "hover":
            return HoverModule(type, config)
        elif type == "input":
            return InputModule(type, config)
        elif type == "email":
            return EmailModule(type, config)
        elif type == "set_storage":
            return SetStorageModule(type, config)
        elif type == "assert":
            return AssertModule(type, config)
        else:
            raise NotImplementedError("Testing-Module '" + type + "' not defined")

    @staticmethod
    def create_module_from_config(config):
        type = config['type']
        return TestsConfig.create_module(type, config)
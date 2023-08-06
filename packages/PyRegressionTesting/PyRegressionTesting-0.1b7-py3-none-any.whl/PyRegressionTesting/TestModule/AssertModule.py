import time

from PyRegressionTesting.TestModule import TestModule
from PyRegressionTesting.Utils.Logger import Logger
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult


class AssertModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)

    def run(self, webDriver, config, lastResult, pre=False):
        success = False
        if self.module_config['assert_type'] == 'url':
            opened_url = webDriver.current_url
            success = (opened_url == self.module_config['value'])

        return TestModuleResult("AssertModule", pre, success, None, None, lastResult)
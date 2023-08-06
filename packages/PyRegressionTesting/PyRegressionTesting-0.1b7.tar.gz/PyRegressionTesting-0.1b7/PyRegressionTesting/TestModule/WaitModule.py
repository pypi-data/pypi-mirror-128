import time

from PyRegressionTesting.TestModule import TestModule
from PyRegressionTesting.Utils.Logger import Logger
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult


class WaitModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)
        self.wait_seconds = self.module_config['wait_seconds']

    def run(self, webDriver, config, lastResult, pre=False):
        if self.wait_seconds > 0:
            Logger.log("Wating for "+str(self.wait_seconds)+" seconds", "WaitModule")
            time.sleep(self.wait_seconds)

        return TestModuleResult("WaitModule", pre, True, None, None, lastResult)
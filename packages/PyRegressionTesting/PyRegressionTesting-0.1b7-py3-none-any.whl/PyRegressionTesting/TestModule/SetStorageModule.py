from datetime import datetime

from PyRegressionTesting.TestModule import TestModule
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult

class SetStorageModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)

    def run(self, webDriver, config, lastResult, pre=False):
        module_result = TestModuleResult("EmailModule", pre, True, None, None, lastResult)

        value = self.module_config['value']
        if "prefix" in self.module_config:
            if self.module_config['prefix'] == "timestamp":
                prefix = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            else:
                prefix = ""
            value = prefix + "-" + value

        module_result.set_result(self.module_config['key'], value)
        return module_result
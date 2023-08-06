from PyRegressionTesting.TestModule import TestModule, FROM_STORAGE
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult


class InputModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)
        self.selector = self.module_config['selector']
        self.input = self.module_config['input']
        self.input_type = self.module_config['input_type']

    def run(self, webDriver, config, lastResult, pre=False):
        msg = None

        if self.input == FROM_STORAGE:
            self.input = self.get_from_storage(lastResult, self.module_config['storage_key'])

        try:
            inputElement = webDriver.find_element_by_css_selector(self.selector)
            inputElement.send_keys(self.input)
            success = True
        except Exception as e:
            success = False
            msg = "Could not find element for input: "+self.selector
            print("Could not find element for input: "+self.selector)
            print(e)

        return TestModuleResult("InputModule", pre, success, msg, None, lastResult)
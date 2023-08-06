import traceback

from selenium.webdriver import ActionChains

from PyRegressionTesting.TestModule import TestModule
from PyRegressionTesting.Utils.Logger import Logger
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult


class HoverModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)

        self.selector = None
        self.id = None
        self.xpath = None

        if "selector" in self.module_config:
            self.selector = self.module_config['selector']

        if "id" in self.module_config:
            self.id = self.module_config['id']

        if "xpath" in self.module_config:
            self.xpath = self.module_config['xpath']

        self.optional = False
        if "optional" in self.module_config:
            self.optional = self.module_config['optional']

    def run(self, webDriver, config, lastResult, pre=False):
        success = False
        msg = None

        try:
            element = None
            if self.selector is not None:
                element = webDriver.find_element_by_css_selector(self.selector)
            elif self.id is not None:
                element = webDriver.find_element_by_id(self.id)
            elif self.xpath is not None:
                element = webDriver.find_element_by_xpath(self.xpath)
            hover = ActionChains(webDriver).move_to_element(element)
            hover.perform()
            success = True
        except Exception as e:
            if self.optional:
                success = True
                msg = "Could not find element to hover (but was optional anyway): "+self.selector
                Logger.log("Could not find element to hover (but was optional anyway): " + self.selector, "HoverModule")
            else:
                msg = "Could not find element to hover: "+self.selector
                print("Could not find element to hover: "+self.selector)
                print(e)

        return TestModuleResult("HoverModule", pre, success, msg, None, lastResult)
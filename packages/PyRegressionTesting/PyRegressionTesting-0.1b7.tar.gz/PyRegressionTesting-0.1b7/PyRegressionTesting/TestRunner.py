from PyRegressionTesting.Utils.Helper import Helper
from PyRegressionTesting.Utils.Logger import Logger


class TestRunner:
    def __init__(self, driver, name, url, pre_steps, test_steps, headless=True):
        self.driver = driver
        self.name = name
        self.url = url
        self.pre_steps = pre_steps
        self.test_steps = test_steps
        self.headless = headless

    def run_test(self, config):
        Logger.log("Running test '"+self.name+"'", "TestRunner")

        webDriver = Helper.createWebDriver(self.driver, self.headless)
        webDriver.get(self.url)

        webDriver.set_window_position(0, 0)
        webDriver.set_window_size(1920, 1080)

        test_results = []

        #Run pre test steps
        last_result = None
        for step in self.pre_steps:
            last_result = step.run(webDriver, config, last_result, pre=True)
            test_results.append(last_result)

        #Run test steps
        last_result = None
        for step in self.test_steps:
            last_result = step.run(webDriver, config, last_result)
            test_results.append(last_result)

        webDriver.close()

        return test_results
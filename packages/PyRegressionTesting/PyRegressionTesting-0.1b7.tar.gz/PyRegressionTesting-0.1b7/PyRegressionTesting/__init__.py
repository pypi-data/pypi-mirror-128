from PyRegressionTesting.TestRunner import TestRunner
from PyRegressionTesting.ThreadWithReturnValue import ThreadWithReturnValue
from PyRegressionTesting.Utils.Helper import Helper
from PyRegressionTesting.TestModule.ClickModule import ClickModule
from PyRegressionTesting.TestModule.WaitModule import WaitModule
from PyRegressionTesting.Utils.RunnerResult import RunnerResult


class PyRegressionTesting:
    def __init__(self, config, driver, threads, logging, headless):
        self.config = config
        self.driver = driver
        self.threads = threads
        self.logging = logging
        self.headless = headless
        pass

    def run_tests(self):
        runners = []
        for test in self.config.tests_config:
            runner = TestRunner(self.driver, test.name, test.url, test.pre_steps, test.test_steps, self.headless)
            runners.append(runner)

        thread_chunks = Helper.split_list(runners, self.threads)

        threads = []
        for chunk in thread_chunks:
            thread = ThreadWithReturnValue(target=self.execute_runners, args=(chunk,self.config,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        results = []
        for thread in threads:
            results.extend(thread.join())

        return results

    def execute_runners(self, runners, config):
        results = []

        for runner in runners:
            test_results = runner.run_test(config)
            results.append(RunnerResult(runner.name, test_results))

        return results

    def print_summary(self, results):
        total = len(results)
        success = 0
        failed = 0

        for result in results:
            if result.was_success():
                success += 1
            else:
                failed += 1

        status_string = "SUCCESS"
        if failed > 0:
            status_string = "FAILED"

        print("#############")
        print("Test set status: "+status_string)
        print("Total tests run: "+str(total))
        print("Successful tests run: "+str(success))
        print("Failed tests: "+str(failed))
        print("#############")


    def was_success(self, results):
        total = len(results)
        success = 0
        failed = 0

        for result in results:
            if result.was_success():
                success += 1
            else:
                failed += 1
        return failed < 1

    def check_results(self, results, send_mail_on_fail=False):
        #Send Mail
        #Log Results
        #Print results pretty
        for result in results:
            print("#############")
            print("Results for '"+result.name+"'")
            for test_result in result.test_results:
                print(test_result.print())
            result.print_summary()
            print("#############")

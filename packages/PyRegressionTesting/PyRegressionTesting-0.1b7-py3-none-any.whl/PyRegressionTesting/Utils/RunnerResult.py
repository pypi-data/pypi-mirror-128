class RunnerResult:
    def __init__(self, name, test_results):
        self.name = name
        self.test_results = test_results

    def get_stats(self):
        total = 0
        success = 0
        failed = 0

        for test_result in self.test_results:
            total += 1
            if test_result.success:
                success += 1
            else:
                failed += 1

        return total, success, failed

    def was_success(self):
        total, success, failed = self.get_stats()

        return failed == 0

    def print_summary(self):
        total, success, failed = self.get_stats()

        print("Total Steps: "+str(total)+" (Successful: "+str(success)+", Failed: "+str(failed)+")")
        if self.was_success():
            print("Test was SUCCESSFUL")
        else:
            print("Test FAILED")
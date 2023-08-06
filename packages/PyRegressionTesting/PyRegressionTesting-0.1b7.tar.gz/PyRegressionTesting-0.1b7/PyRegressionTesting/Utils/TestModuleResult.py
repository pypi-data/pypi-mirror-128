from PyRegressionTesting.Utils.Logger import Logger


class TestModuleResult:
    def __init__(self, module_name, pre, success, msg=None, params=None, last_result=None):
        self.module_name = module_name
        self.pre = pre
        self.success = success
        self.msg = msg
        self.params = params

        self.result = {}
        if last_result is not None:
            self.result = last_result.result

    def set_result(self, storage_key, storage_value):
        Logger.log("Setting storage: '"+storage_key+"' => "+str(storage_value))
        self.result[storage_key] = storage_value

    def print(self):
        success_str = "successful"
        if not self.success:
            success_str = "NOT successful"

        prefix = ""
        if self.pre:
            prefix = "[PRE-TEST] "

        message = prefix + self.module_name+" was "+success_str

        if self.msg is not None or self.params is not None or self.result is not None:
            message += ":"

            if self.msg is not None:
                message += " " + self.msg

            if self.params is not None:
                message += " (" + str(self.params) + ")"

            if self.result is not None:
                message += " (Result: " + str(self.result) + ")"

        return message
FROM_STORAGE = "{{FROM_STORAGE}}"

class TestModule:
    def __init__(self, type, module_config):
        self.type = type
        self.module_config = module_config

    def run(self, webDriver, config, lastResult, pre=False):
        raise NotImplementedError()

    def get_last_result(self, lastResult):
        if lastResult is None:
            raise AttributeError("Last Result should be used but is None")
        return lastResult.result

    def get_from_storage(self, lastResult, storageKey):
        if lastResult is not None and lastResult.result is not None and storageKey in lastResult.result:
            return lastResult.result[storageKey]
        else:
            return None
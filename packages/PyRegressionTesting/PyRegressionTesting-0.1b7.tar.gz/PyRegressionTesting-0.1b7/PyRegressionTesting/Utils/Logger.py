from datetime import datetime

LOGGING = False

class Logger:
    @staticmethod
    def log(msg, module=None):
        if not LOGGING:
            return

        now = datetime.now()

        module_string = ""
        if module is not None:
            module_string = module + "\t"

        print(str(module_string) + "[" + str(now.strftime("%d.%m.%Y %H:%M:%S")) + "] | " + str(msg))
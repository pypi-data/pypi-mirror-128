import imaplib
import re

from PyRegressionTesting.TestModule import TestModule, FROM_STORAGE
from PyRegressionTesting.Utils.TestModuleResult import TestModuleResult

class EmailModule(TestModule):
    def __init__(self, type, module_config):
        super().__init__(type, module_config)
        self.task = self.module_config['task']

    def run(self, webDriver, config, lastResult, pre=False):
        success = False
        msg = None
        params = None
        result = None

        to_mail = self.module_config['to_mail']
        if to_mail == FROM_STORAGE:
            to_mail = self.get_from_storage(lastResult, self.module_config['load_storage_key'])

        if self.task == "get_content":
            email = self.find_latest_email(config.receiver_mail_config, to_mail, self.module_config['subject'])
            result = self.find_content_in_mail(email, self.module_config['pattern'])
        else:
            raise AttributeError("Unknown Mail-Task: "+self.task)

        if result is not None:
            success = True

        module_result = TestModuleResult("EmailModule", pre, success, msg, params, lastResult)
        module_result.set_result(self.module_config['set_storage_key'], result)
        return module_result

    def find_latest_email(self, receiver_config, to_mail, subject):
        mail = imaplib.IMAP4_SSL(receiver_config.host)
        mail.login(receiver_config.user, receiver_config.password)
        mail.list()
        mail.select("inbox")

        result, data = mail.search(None, '(TO "' + to_mail + '" SUBJECT "' + subject + '" UNSEEN)')

        ids = data[0]
        id_list = ids.split()

        if len(id_list) < 1:
            return None

        latest_email_id = id_list[-1]

        result, data = mail.fetch(latest_email_id, "(RFC822)")

        raw_email = data[0][1]
        return str(raw_email)

    def find_content_in_mail(self, email, pattern):
        password_pattern = re.compile(pattern)
        matches = password_pattern.findall(email)
        if len(matches) > 0:
            return matches[0]
        else:
            return None
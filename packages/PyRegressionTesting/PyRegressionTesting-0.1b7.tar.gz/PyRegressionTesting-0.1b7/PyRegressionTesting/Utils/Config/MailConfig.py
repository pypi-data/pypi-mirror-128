class MailConfig:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    @staticmethod
    def from_json(json):
        host = json['smtp_host']
        port = json['smtp_port']
        user = json['smtp_user']
        password = json['smtp_pass']

        return MailConfig(host, port, user, password)
class ParsingErrorExceptions(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

class ValidationErrorExceptions(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

class SendMailException(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message
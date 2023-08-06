
class WebsupportError(Exception):
    def __init__(self, message, code=None, body=None):
        Exception.__init__(self, message)
        self.message = message
        self.code = code
        self.body = body

    def __str__(self):
        if self.code is not None:
            return f"{self.code}: {self.message}"
        else:
            return f"{self.message}"


class WebsupportAuthenticationError(WebsupportError):
    pass


class WebsupportZoneNotFound(WebsupportError):
    pass


class WebsupportConnectionError(WebsupportError):
    pass


class WebsupportIDNotFoundError(WebsupportError):
    pass


class WebsupportAPIError(WebsupportError):
    pass

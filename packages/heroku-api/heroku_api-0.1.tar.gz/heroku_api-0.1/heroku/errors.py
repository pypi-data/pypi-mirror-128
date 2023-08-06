class RateLimitExceded(Exception):
    """
        Rate Limit Exception
        Called when heroku api
        reaches the maximium
        requests rate
    """
    text: str = "Api Rate Limit Exceded, please wait"

    def _exec(self=None):
        return RateLimitExceded(RateLimitExceded.text)


class InvalidRequest(Exception):
    pass


class Message(Exception):
    pass


class Error(Exception):
    """
        More general exception
    """
    pass


class InvalidAPIKey(Exception):
    """
        Raised when the user give's
        an invalid Api key
    """
    def _exec(self: Exception = None):
        return InvalidAPIKey("Invalid API Key!")


common = {
    "-1": InvalidRequest("Request not completed correctly [-1]"),
    "-2": RateLimitExceded._exec(),
    "-3": InvalidAPIKey._exec()
}

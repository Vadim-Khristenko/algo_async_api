class AsyncDefaultException(Exception):
    def __init__(self, message):
        super().__init__(message)

class AsyncUnknownException       (AsyncDefaultException): pass
class AsyncSessionClosed          (AsyncDefaultException): pass
class AsyncInvalidCredentials     (AsyncDefaultException): pass
class AsyncNotImplementedException(AsyncDefaultException): pass
class AsyncAlreadyLoggedIn        (AsyncDefaultException): pass
class AsyncCommentIdUnspecified   (AsyncDefaultException): pass
class AsyncCommentNotFound        (AsyncDefaultException): pass
class AsyncProjectIdUnspecified   (AsyncDefaultException): pass
class AsyncReactionUnspecified    (AsyncDefaultException): pass
class AsyncCodeUnspecified        (AsyncDefaultException): pass
class AsyncUserIdUnspecified      (AsyncDefaultException): pass

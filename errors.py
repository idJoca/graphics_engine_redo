

class NonUniqueIdentifierError(BaseException):
    """ 
    Raised when a identifier is non unique
    """
    pass


class InexistentIdentifierError(BaseException):
    """ 
    Raised when a given identifier isn't associated to anything
    """
    pass


class InvalidVectorError(BaseException):
    """ 
    Raised when a given vector don't match the expected
    """
    pass


class NoLightsLoadedError(BaseException):
    """ 
    Raised when a scene is rendered without any light sources
    """
    pass

'''
All custom exceptions raised in the project.
'''


class InvalidWidgetDefinition(ValueError):
    pass


class InvalidLayoutError(Exception):
    pass


class InvalidCallbackDefinition(Exception):
    def __init__(self, msg: str):
        self.msg = msg

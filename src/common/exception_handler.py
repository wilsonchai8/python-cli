from .const import *

class ParamError(Exception):
    def __init__(self, msg="", code=PARAM_ERROR):
        super().__init__(msg, code)
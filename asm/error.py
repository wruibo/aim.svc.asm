"""
    error definition
"""


class UserError(Exception):
    pass


class SysError(Exception):
    pass


USER_ACCESS_INVALID = UserError('非法访问')
USER_PARAM_INVALID = UserError('非法访问参数')

SYSTEM_ERROR = SysError('系统错误')

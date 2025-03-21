class UserNotFoundException(Exception):
    detail = "User not found"


class IncorrectPassword(Exception):
    detail = "Password is not correct"


class TokenExpired(Exception):
    detail = "Tokend has expired"


class TokenNotCorrect(Exception):
    detail = "Token is not correct"


class TaskNotCorrect(Exception):
    detail = "Token is not correct"

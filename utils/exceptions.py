# utils/exceptions.py

class EmployeeSystemException(Exception):
    """従業員システムの基本例外クラス。"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseException(EmployeeSystemException):
    """データベース関連の例外クラス。"""
    pass

class ValidationException(EmployeeSystemException):
    """入力検証関連の例外クラス。"""
    pass

class NotFoundException(EmployeeSystemException):
    """リソースが見つからない場合の例外クラス。"""
    pass

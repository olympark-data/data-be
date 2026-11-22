class AppException(Exception):
    """서비스에서 던지는 예외의 부모. 전역 핸들러가 ApiResponse로 바꿔 돌려준다."""

    status_code = 400
    code = "BAD_REQUEST"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundException(AppException):
    status_code = 404
    code = "NOT_FOUND"

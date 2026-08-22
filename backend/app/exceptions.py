class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400, error_code: str = "BAD_REQUEST"):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.detail)

class AuthenticationError(AppException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, status_code=401, error_code="UNAUTHORIZED")

class AuthorizationError(AppException):
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(detail=detail, status_code=403, error_code="FORBIDDEN")

class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404, error_code="NOT_FOUND")

class ValidationError(AppException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail=detail, status_code=422, error_code="VALIDATION_ERROR")

class FileProcessingError(AppException):
    def __init__(self, detail: str = "Error processing file"):
        super().__init__(detail=detail, status_code=400, error_code="FILE_PROCESSING_ERROR")

class AIServiceError(AppException):
    def __init__(self, detail: str = "AI service error"):
        super().__init__(detail=detail, status_code=503, error_code="AI_SERVICE_ERROR")

class DatabaseError(AppException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(detail=detail, status_code=500, error_code="DATABASE_ERROR")

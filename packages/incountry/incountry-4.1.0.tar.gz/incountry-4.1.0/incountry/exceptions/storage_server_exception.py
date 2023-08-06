from .storage_exception import StorageException


class StorageServerException(StorageException):
    def __init__(self, message, status_code=None):
        super(StorageException, self).__init__(message)

        self.status_code = status_code


class StorageNetworkException(StorageServerException):
    pass


class StorageServerResponseValidationException(StorageServerException):
    pass


class StorageAuthenticationException(StorageServerException):
    pass

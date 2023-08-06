import abc
import re

from graphql import GraphQLError


class InitCommerceBaseException(GraphQLError, metaclass=abc.ABCMeta):
    path = None
    locations = None
    original_error = None
    message = "INIT_COMMERCE_BASE_EXCEPTION"
    hint: str = None

    @property
    def code(self) -> str:
        class_name = self.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).upper()

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message=message or self.message, *args, **kwargs)

        errorcode = self.code.replace(" ", "_").upper()

        self.extensions = dict(
            code=errorcode,
            hint=self.hint,
        )

    def __repr__(self) -> str:
        return self.extensions


class InternalServerError(InitCommerceBaseException):
    code = "INTERNAL_SERVER_ERROR"

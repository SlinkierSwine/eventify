import logging
from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: Any) -> Response:
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        response = Response(
            {
                "status_code": 500,
                "detail": "Internal Server Error",
            },
            500,
            content_type="application/json",
        )
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    logger.error(exc, exc_info=True)

    return response

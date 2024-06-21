import datetime
from typing import Any
from urllib.parse import parse_qsl, urlparse

from django.urls import reverse
from django.utils.http import urlencode


def get_tomorrow_date() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=1)


def get_yesterday_date() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)


def patch_url(url: str, **kwargs: Any) -> str:
    """Replace or add query params in url"""
    return (
        urlparse(url)
        ._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs)))
        .geturl()
    )


def reverse_with_query_params(
    url: str, query_params: dict[str, Any], kwargs: dict[str, Any]
) -> str:
    return patch_url(reverse(url, kwargs=kwargs), **query_params)

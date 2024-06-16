import datetime

from drf_spectacular.utils import OpenApiExample


now_dt = datetime.datetime.now(datetime.UTC)

create_event_examples = [
    OpenApiExample(
        "Example 1",
        value={
            "name": "Test event",
            "description": "It is a test event",
            "start_datetime": now_dt + datetime.timedelta(days=1),
            "end_datetime": now_dt + datetime.timedelta(days=1, hours=1),
            "is_private": False,
        },
        request_only=True,
    )
]

from drf_spectacular.utils import OpenApiExample


registration_examples = [
    OpenApiExample(
        "Example 1",
        value={"username": "testuser", "password": "TestPassword123"},
        request_only=True,
    )
]


login_examples = [
    OpenApiExample(
        "Example 1",
        value={"username": "testuser", "password": "TestPassword123"},
        request_only=True,
    )
]

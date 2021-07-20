from django.core.exceptions import ValidationError


def validate_tasty(value):
    if not value.startswith("Tasty"):
        msg = "Must start with Tasty"
        raise ValidationError(msg)
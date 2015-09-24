from django.core.exceptions import ValidationError

import re


def integer_only(value):
    pattern = "^[0-9]+$"
    if not re.match(pattern, str(value)):
        raise ValidationError(u'%s ist keine Zahl!' % value)
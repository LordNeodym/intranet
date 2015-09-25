from django.core.exceptions import ValidationError

import re


def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Nur eine Instanz von %s erlaubt!" % model.__name__)


def integer_only(value):
    pattern = "^[0-9]+$"
    if not re.match(pattern, str(value)):
        raise ValidationError(u'%s ist keine Zahl!' % value)
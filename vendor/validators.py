import os
from django.core.exceptions import ValidationError


def allow_image_only_validator(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_ext = [".jpg", ".png", ".jpeg"]
    if not ext.lower() in valid_ext:
        raise ValidationError("Unsupported file extension: Supported extensions"+ str(valid_ext))
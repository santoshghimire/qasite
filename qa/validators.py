import os

from django.core.exceptions import ValidationError


def validate_image(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg']
    valid_size = 2621440  # 2 MB
    if ext.lower() not in valid_extensions:
        raise ValidationError(
            u'Unsupported file extension. upload .jpg, .jpeg or .png')
    else:
        if value.size > valid_size:
            raise ValidationError("Image file too large. Size limit is 2MB")


def validate_audio(value):
    valid_size = 5242880
    if value.size > valid_size:
        raise ValidationError("Audio file too large. Upload up to 5MB")


def validate_file(value):
    valid_size = 5242880
    if value.size > valid_size:
        raise ValidationError("File too large. Upload up to 5MB")


def validate_video(value):
    valid_size = 10485760
    if value.size > valid_size:
        raise ValidationError("Video file too large. Upload up to 10MB")

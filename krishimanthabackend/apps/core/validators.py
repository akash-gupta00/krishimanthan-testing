import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size_mb=25):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        if not value:
            return

        # Safe attribute lookup to handle NoneType from Cloudinary / storage backend
        file_size = getattr(value, "size", None)
        if file_size is not None and file_size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(
                f"File size must not exceed {self.max_size_mb} MB."
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator)
            and self.max_size_mb == other.max_size_mb
        )


@deconstructible
class FileExtensionValidator:
    def __init__(self, allowed_extensions=None):
        if allowed_extensions is None:
            allowed_extensions = ["pdf", "jpg", "jpeg", "png", "webp"]
        self.allowed_extensions = [ext.lower().lstrip(".") for ext in allowed_extensions]

    def __call__(self, value):
        if not value:
            return

        ext = os.path.splitext(getattr(value, "name", ""))[1].lower().lstrip(".")
        if ext not in self.allowed_extensions:
            raise ValidationError(
                f"Unsupported file format (.{ext}). Allowed formats: {', '.join(self.allowed_extensions)}"
            )

    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionValidator)
            and self.allowed_extensions == other.allowed_extensions
        )


# Direct instances
validate_pdf_extension = FileExtensionValidator(allowed_extensions=["pdf"])
validate_image_extension = FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
validate_file_size = FileSizeValidator(max_size_mb=25)

# Backward-compatible function validators (required by sitesettings and models)
def validate_image_file(value):
    validate_image_extension(value)
    validate_file_size(value)


def validate_pdf_file(value):
    validate_pdf_extension(value)
    validate_file_size(value)
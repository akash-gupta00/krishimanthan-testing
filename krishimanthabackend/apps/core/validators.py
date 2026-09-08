"""
Upload security validators.

Anything a public form can upload (ad images/PDFs, and any file an admin
uploads) is validated here: file extension AND the file's actual binary
signature are checked — not just the extension — so a malicious file
renamed to look like an image or PDF (e.g. a `.php` or `.html` file saved
as `photo.jpg`) is rejected rather than silently stored and later served
back to visitors' browsers.
"""
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

MAX_IMAGE_SIZE_MB = 5
MAX_PDF_SIZE_MB = 20
MAX_DOCUMENT_SIZE_MB = 20

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}


@deconstructible
class ImageFileValidator:
    """Validates an ImageField upload is really an image: allowed
    extension, under the size limit, and openly parseable by Pillow
    (catches files that merely have an image extension)."""

    def __init__(self, max_size_mb=MAX_IMAGE_SIZE_MB):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        ext = value.name.rsplit(".", 1)[-1].lower() if "." in value.name else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}.")

        if value.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f"Image too large — max {self.max_size_mb}MB.")

        try:
            from PIL import Image
            value.seek(0)
            img = Image.open(value)
            img.verify()  # raises if not a genuine, undamaged image
        except Exception:
            raise ValidationError("This file is not a valid image (its content doesn't match an image format).")
        finally:
            value.seek(0)


@deconstructible
class PDFFileValidator:
    """Validates a FileField upload is really a PDF: .pdf extension,
    under the size limit, and starts with the real PDF magic bytes."""

    def __init__(self, max_size_mb=MAX_PDF_SIZE_MB):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        if not value.name.lower().endswith(".pdf"):
            raise ValidationError("Only .pdf files are allowed.")

        if value.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f"File too large — max {self.max_size_mb}MB.")

        value.seek(0)
        header = value.read(5)
        value.seek(0)
        if header != b"%PDF-":
            raise ValidationError("This file is not a valid PDF (its content doesn't match the PDF format).")


validate_image_file = ImageFileValidator()
validate_pdf_file = PDFFileValidator()

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
from django.core.files.uploadedfile import UploadedFile

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
        if not value or not getattr(value, "name", None):
            return

        # Check agar file naye upload ke roop me aayi hai ya purani saved file hai
        is_new_upload = isinstance(value, UploadedFile)

        ext = value.name.rsplit(".", 1)[-1].lower() if "." in value.name else ""
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}.")

        # Safe size check (Render redeploy hone par disk par purani file missing ho sakti hai)
        try:
            if value.size > self.max_size_mb * 1024 * 1024:
                raise ValidationError(f"Image too large — max {self.max_size_mb}MB.")
        except (FileNotFoundError, OSError):
            # File system par file nahi hai (ephemeral disk wipe), crash mat hone do
            if not is_new_upload:
                return
            raise ValidationError("File could not be found or read.")

        # Binary parse check
        try:
            from PIL import Image
            value.seek(0)
            img = Image.open(value)
            img.verify()  # raises if not a genuine, undamaged image
            value.seek(0)
        except (FileNotFoundError, OSError):
            if not is_new_upload:
                return
            raise ValidationError("Unable to read image content.")
        except Exception:
            raise ValidationError("This file is not a valid image (its content doesn't match an image format).")
        finally:
            try:
                value.seek(0)
            except Exception:
                pass


@deconstructible
class PDFFileValidator:
    """Validates a FileField upload is really a PDF: .pdf extension,
    under the size limit, and starts with the real PDF magic bytes."""

    def __init__(self, max_size_mb=MAX_PDF_SIZE_MB):
        self.max_size_mb = max_size_mb

    def __call__(self, value):
        if not value or not getattr(value, "name", None):
            return

        is_new_upload = isinstance(value, UploadedFile)

        if not value.name.lower().endswith(".pdf"):
            raise ValidationError("Only .pdf files are allowed.")

        try:
            if value.size > self.max_size_mb * 1024 * 1024:
                raise ValidationError(f"File too large — max {self.max_size_mb}MB.")
        except (FileNotFoundError, OSError):
            if not is_new_upload:
                return
            raise ValidationError("File could not be found or read.")

        try:
            value.seek(0)
            header = value.read(5)
            value.seek(0)
            if header != b"%PDF-":
                raise ValidationError("This file is not a valid PDF (its content doesn't match the PDF format).")
        except (FileNotFoundError, OSError):
            if not is_new_upload:
                return
            raise ValidationError("Unable to read PDF content.")


validate_image_file = ImageFileValidator()
validate_pdf_file = PDFFileValidator()
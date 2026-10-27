import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi import HTTPException, UploadFile
from PIL import Image
from starlette.datastructures import Headers

from app import image_validation


def photo_bytes(format="PNG", size=(10, 10)):
    buffer = io.BytesIO()
    Image.new("RGB", size, "pink").save(buffer, format=format)
    return buffer.getvalue()


def upload(data, filename="photo.png", mime="image/png"):
    return UploadFile(io.BytesIO(data), filename=filename, headers=Headers({"content-type": mime}))


class ImageValidationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.output = Path(self.folder.name) / "saved-photo"

    def assert_rejected(self, file, status):
        with self.assertRaises(HTTPException) as failure:
            image_validation.save_validated_photo(file, self.output)
        self.assertEqual(failure.exception.status_code, status)
        self.assertFalse(self.output.exists())

    def test_jpeg_png_and_webp_are_accepted(self):
        for format, filename, mime in [("JPEG", "photo.JPG", "image/jpeg"), ("PNG", "photo.png", "image/png"), ("WEBP", "photo.webp", "image/webp")]:
            with self.subTest(format=format):
                data = photo_bytes(format)
                image_validation.save_validated_photo(upload(data, filename, mime), self.output)
                self.assertEqual(self.output.read_bytes(), data)

    def test_exactly_ten_megabytes_is_accepted(self):
        data = photo_bytes()
        data += b"\0" * (image_validation.MAX_FILE_BYTES - len(data))
        image_validation.save_validated_photo(upload(data), self.output)
        self.assertEqual(self.output.stat().st_size, image_validation.MAX_FILE_BYTES)

    def test_over_ten_megabytes_is_rejected_and_partial_file_removed(self):
        self.assert_rejected(upload(b"x" * (image_validation.MAX_FILE_BYTES + 1)), 413)

    def test_empty_file_is_rejected(self):
        self.assert_rejected(upload(b""), 400)

    def test_fake_image_is_rejected(self):
        self.assert_rejected(upload(b"This is not a photograph"), 400)

    def test_wrong_extension_and_disallowed_format_are_rejected(self):
        self.assert_rejected(upload(photo_bytes(), "photo.jpg", "image/jpeg"), 400)
        self.assert_rejected(upload(photo_bytes("GIF"), "photo.gif", "image/gif"), 400)

    def test_truncated_file_is_rejected(self):
        self.assert_rejected(upload(photo_bytes()[:35]), 400)

    def test_pixel_limit_is_checked_before_processing(self):
        with patch.object(image_validation, "MAX_IMAGE_PIXELS", 100):
            image_validation.save_validated_photo(upload(photo_bytes(size=(10, 10))), self.output)
            self.output.unlink()
            self.assert_rejected(upload(photo_bytes(size=(11, 10))), 413)


if __name__ == "__main__":
    unittest.main()

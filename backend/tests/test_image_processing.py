import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from app import image_processing


class ImageProcessingTests(unittest.TestCase):
    def test_large_photo_is_bounded_and_exported_as_rgba(self):
        with tempfile.TemporaryDirectory() as folder:
            source, destination = Path(folder) / "photo.jpg", Path(folder) / "result.png"
            Image.new("RGB", (2400, 1600), "red").save(source)
            session = object()
            with (
                patch.object(image_processing, "_background_session", return_value=session),
                patch.object(image_processing, "remove", side_effect=lambda image, **kwargs: image.convert("RGBA")) as remove,
            ):
                image_processing.prepare_foreground(source, destination)
            supplied = remove.call_args.args[0]
            self.assertLessEqual(max(supplied.size), 1024)
            self.assertEqual(remove.call_args.kwargs["session"], session)
            with Image.open(destination) as result:
                self.assertEqual(result.mode, "RGBA")
                self.assertEqual(result.format, "PNG")

    def test_lightweight_session_is_reused(self):
        image_processing._background_session.cache_clear()
        try:
            with patch.object(image_processing, "new_session") as create:
                first = image_processing._background_session()
                second = image_processing._background_session()
            self.assertIs(first, second)
            create.assert_called_once()
            self.assertEqual(create.call_args.args, ("u2netp",))
            self.assertFalse(create.call_args.kwargs["sess_opts"].enable_cpu_mem_arena)
        finally:
            image_processing._background_session.cache_clear()


if __name__ == "__main__":
    unittest.main()

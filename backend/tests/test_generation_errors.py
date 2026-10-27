import unittest

from app.generation_errors import describe_generation_error


class GenerationErrorTests(unittest.TestCase):
    def test_onnx_memory_error_is_not_a_quota_error(self):
        status, message = describe_generation_error(RuntimeError(
            "[ONNXRuntimeError] BFCArena::AllocateRawInternal Failed to allocate memory "
            "for requested buffer of size 822083584"
        ))
        self.assertEqual(status, 503)
        self.assertIn("оперативной памяти", message)
        self.assertNotIn("осталось", message)
        self.assertNotIn("822083584", message)

    def test_python_memory_error(self):
        self.assertEqual(describe_generation_error(MemoryError())[0], 503)

    def test_quota_wait_time_comes_from_service(self):
        status, message = describe_generation_error(RuntimeError(
            "You have exceeded your ZeroGPU quota (60s requested vs. 56s left). "
            "Try again in 18:12:24. Authenticate with a Hugging Face token"
        ))
        self.assertEqual(status, 429)
        self.assertIn("18 ч 12 мин 24 с", message)

    def test_missing_reset_time_is_not_invented(self):
        status, message = describe_generation_error(RuntimeError("ZeroGPU quota exceeded"))
        self.assertEqual(status, 429)
        self.assertIn("не сообщил", message)

    def test_unrelated_error_keeps_diagnostic(self):
        status, message = describe_generation_error(ValueError("Model not found"))
        self.assertEqual(status, 502)
        self.assertIn("Model not found", message)


if __name__ == "__main__":
    unittest.main()

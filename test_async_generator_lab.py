import asyncio
import unittest

from async_generator_lab import closable_stream, numbers


class AsyncGeneratorTests(unittest.IsolatedAsyncioTestCase):
    async def test_numbers_yield_expected_values(self):
        result = [value async for value in numbers(3)]
        self.assertEqual(result, [1, 2, 3])

    async def test_aclose_runs_finally(self):
        cleaned = []
        stream = closable_stream(cleaned)
        self.assertEqual(await anext(stream), "alpha")
        await stream.aclose()
        self.assertEqual(cleaned, [True])


if __name__ == "__main__":
    unittest.main()

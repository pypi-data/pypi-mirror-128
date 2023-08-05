import unittest
import loop


class MyTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(loop.add(), 2)

    def test_sub(self):
        self.assertEqual(loop.sub(), 2)


if __name__ == '__main__':
    unittest.main()

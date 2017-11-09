# Set the path
import os
import sys
import unittest
from app.tests import AppTest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


if __name__ == '__main__':
    unittest.main()
